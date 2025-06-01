import asyncio
import json
import logging
import uuid

from aio_pika import IncomingMessage, Message, DeliveryMode, ExchangeType


from .db.sessions import async_session
from .schemas.user_schemas import UserIn, UserUpdateIn
from .services import user_service

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.INFO)


async def handle_message_add(message: IncomingMessage):
    async with message.process():
        try:
            data = json.loads(message.body)
            author_data = UserIn(
                id=data["id"],
                first_name=data["first_name"],
                last_name=data["last_name"],
            )
        except Exception as e:
            logger.error(f"Failed to parse user data from message: {e}", exc_info=True)
            return

        try:
            async with async_session() as session:
                author = await user_service.create_user(session, author_data)
        except Exception as e:
            logger.error(f"Failed to create user: {e}", exc_info=True)

async def handle_message_update(message: IncomingMessage):
    async with message.process():
        try:
            data = json.loads(message.body)
            author_data = UserUpdateIn(
                first_name=data["first_name"],
                last_name=data["last_name"],
            )
        except Exception as e:
            logger.error(f"Failed to parse user data from message: {e}", exc_info=True)
            return

        try:
            async with async_session() as session:
                author = await user_service.update_user(session, data["id"], author_data)
        except Exception as e:
            logger.error(f"Failed to update author: {e}", exc_info=True)

async def handle_message_delete(message: IncomingMessage):
    async with message.process():
        try:
            data = json.loads(message.body)
        except Exception as e:
            logger.error(f"Failed to parse user data from message: {e}", exc_info=True)
            return

        try:
            async with async_session() as session:
                check = await user_service.delete_user(session, data["id"])
        except Exception as e:
            logger.error(f"Failed to update user: {e}", exc_info=True)


async def handler():
    from .main import rabbit_channel, user_channel
    exchange_add = await user_channel.declare_exchange(name="register_user",type=ExchangeType.FANOUT, durable=True)
    exchange_update = await user_channel.declare_exchange(name="update_user", type=ExchangeType.FANOUT, durable=True)
    exchange_delete = await user_channel.declare_exchange(name="delete_user", type=ExchangeType.FANOUT, durable=True)

    queue_add = await rabbit_channel.declare_queue(name="register_queue_dis",durable=True)
    queue_update = await rabbit_channel.declare_queue(name="update_queue_dis",durable=True)
    queue_delete = await rabbit_channel.declare_queue(name="delete_queue_dis",durable=True)

    await queue_add.bind(exchange_add)
    await queue_update.bind(exchange_update)
    await queue_delete.bind(exchange_delete)

    await queue_add.consume(handle_message_add)
    await queue_update.consume(handle_message_update)
    await queue_delete.consume(handle_message_delete)

    await asyncio.Future()