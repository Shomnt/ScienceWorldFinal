import asyncio

from aio_pika import connect_robust
from fastapi import FastAPI

from .graph_router import graph_router
from .rabbit import get_handler

app = FastAPI()
app.include_router(graph_router, prefix="/area", tags=["area"])

async def main():
    connection = await connect_robust("amqp://guest:guest@rabbitmq-service:5672/")
    channel = await connection.channel()
    queue = await channel.declare_queue("graph_data", durable=True)
    handler = get_handler()
    await queue.consume(handler, no_ack=False)
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
