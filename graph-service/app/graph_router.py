from fastapi import APIRouter
from fastapi.params import Depends
from neo4j import AsyncSession

from .session import get_db
from .edge_schema import EdgeGetOut, EdgeGetIn
from .graph_service import get_value

graph_router = APIRouter()

@graph_router.get("/get/addition", response_model=EdgeGetOut)
async def get_addition(addition_in: EdgeGetIn, db: AsyncSession = Depends(get_db)):
    value = await get_value(db, addition_in)
    return value
