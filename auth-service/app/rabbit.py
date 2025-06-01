import json
from aio_pika import connect_robust, Message, ExchangeType
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel

class AsyncRabbitMQ:
    def __init__(self):
        self.connection: AbstractRobustConnection | None = None
        self.channel: AbstractRobustChannel | None = None

    async def connect(self):
        self.connection = await connect_robust("amqp://guest:guest@rabbitmq-service:5672/")
        self.channel = await self.connection.channel()

    async def send_broadcast(self, exchange_name: str, message_data: dict):
        exchange = await self.channel.declare_exchange(
            name=exchange_name,
            type=ExchangeType.FANOUT,
            durable=True
        )
        message = Message(
            body=json.dumps(message_data).encode(),
            delivery_mode=2
        )

        await exchange.publish(message, routing_key="")

    async def close(self):
        if self.connection:
            await self.connection.close()


rabbitmq_instance: AsyncRabbitMQ | None = AsyncRabbitMQ()