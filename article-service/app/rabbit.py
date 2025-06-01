import asyncio
import json
import logging
import uuid

from aio_pika import IncomingMessage, Message, DeliveryMode, ExchangeType


from .db.sessions import async_session
from .schemas.author_schemas import AuthorIn, AuthorUpdateIn
from .services import author_service

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.INFO)

async def send_rpc_request(data: dict, queue_name: str = "graph_data") -> dict:
    correlation_id = str(uuid.uuid4())

    from .main import rabbit_channel
    callback_queue = await rabbit_channel.declare_queue(exclusive=True)
    future = asyncio.get_event_loop().create_future()

    async def on_response(message: IncomingMessage):
        if message.correlation_id == correlation_id:
            future.set_result(json.loads(message.body))

    await callback_queue.consume(on_response, no_ack=True)

    await rabbit_channel.default_exchange.publish(
        Message(
            body=json.dumps(data).encode(),
            correlation_id=correlation_id,
            reply_to=callback_queue.name,
            delivery_mode=DeliveryMode.PERSISTENT,
        ),
        routing_key=queue_name
    )

    return await future

async def handle_message_add(message: IncomingMessage):
    async with message.process():
        try:
            data = json.loads(message.body)
            author_data = AuthorIn(
                id=data["id"],
                first_name=data["first_name"],
                last_name=data["last_name"],
            )
        except Exception as e:
            logger.error(f"Failed to parse author data from message: {e}", exc_info=True)
            return

        try:
            async with async_session() as session:
                author = await author_service.create_author(session, author_data)
        except Exception as e:
            logger.error(f"Failed to create author: {e}", exc_info=True)

async def handle_message_update(message: IncomingMessage):
    async with message.process():
        try:
            data = json.loads(message.body)
            author_data = AuthorUpdateIn(
                first_name=data["first_name"],
                last_name=data["last_name"],
            )
        except Exception as e:
            logger.error(f"Failed to parse author data from message: {e}", exc_info=True)
            return

        try:
            async with async_session() as session:
                author = await author_service.update_author(session, data["id"], author_data)
        except Exception as e:
            logger.error(f"Failed to update author: {e}", exc_info=True)

async def handle_message_delete(message: IncomingMessage):
    async with message.process():
        try:
            data = json.loads(message.body)
        except Exception as e:
            logger.error(f"Failed to parse author data from message: {e}", exc_info=True)
            return

        try:
            async with async_session() as session:
                check = await author_service.delete_author(session, data["id"])
        except Exception as e:
            logger.error(f"Failed to update author: {e}", exc_info=True)


async def handler():
    from .main import rabbit_channel, user_channel
    exchange_add = await user_channel.declare_exchange(name="register_user",type=ExchangeType.FANOUT, durable=True)
    exchange_update = await user_channel.declare_exchange(name="update_user", type=ExchangeType.FANOUT, durable=True)
    exchange_delete = await user_channel.declare_exchange(name="delete_user", type=ExchangeType.FANOUT, durable=True)

    queue_add = await rabbit_channel.declare_queue(name="register_queue",durable=True)
    queue_update = await rabbit_channel.declare_queue(name="update_queue",durable=True)
    queue_delete = await rabbit_channel.declare_queue(name="delete_queue",durable=True)

    await queue_add.bind(exchange_add)
    await queue_update.bind(exchange_update)
    await queue_delete.bind(exchange_delete)

    await queue_add.consume(handle_message_add)
    await queue_update.consume(handle_message_update)
    await queue_delete.consume(handle_message_delete)

    await asyncio.Future()