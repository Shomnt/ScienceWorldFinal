from contextlib import asynccontextmanager

from fastapi import FastAPI
from .user_router import user_router
from .rabbit import rabbitmq_instance


@asynccontextmanager
async def lifespan(app_main: FastAPI):

    await rabbitmq_instance.connect()
    yield
    await rabbitmq_instance.close()

app = FastAPI(lifespan=lifespan)
app.include_router(user_router, prefix="/auth-service", tags=["user"])