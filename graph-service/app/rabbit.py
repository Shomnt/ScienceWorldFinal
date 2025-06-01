import json
from aio_pika import IncomingMessage, DeliveryMode
from fastapi import Depends
from neo4j import AsyncSession

from .session import get_db
from .edge_schema import EdgeGetIn, EdgeGetOut
from .graph_service import get_value


def get_handler(db: AsyncSession = Depends(get_db)):
    async def handler(message: IncomingMessage):
        async with message.process():
            data = json.loads(message.body)
            try:
                edge_in = EdgeGetIn(**data)
                result: EdgeGetOut = await get_value(db, edge_in)

                response_data = result.model_dump()
            except Exception as e:
                print("Ошибка обработки:", e)
                response_data = {"error": str(e)}

            await message.reply(
                json.dumps(response_data).encode(),
                correlation_id=message.correlation_id,
                delivery_mode=DeliveryMode.PERSISTENT
            )
    return handler
