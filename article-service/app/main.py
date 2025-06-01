import asyncio
from contextlib import asynccontextmanager

from aio_pika import connect_robust
from fastapi import FastAPI

from .routers.article_router import article_router

rabbit_connection = None
rabbit_channel = None
user_channel = None

@asynccontextmanager
async def lifespan(app_main: FastAPI):
    global rabbit_connection, rabbit_channel, user_channel

    rabbit_connection = await connect_robust("amqp://guest:guest@rabbitmq-service:5672/")
    rabbit_channel = await rabbit_connection.channel()
    user_channel = await rabbit_connection.channel()

    from .rabbit import handler
    loop = asyncio.get_event_loop()
    loop.create_task(handler())

    yield

    await rabbit_channel.close()
    await rabbit_connection.close()

app = FastAPI(lifespan=lifespan)
app.include_router(article_router)
