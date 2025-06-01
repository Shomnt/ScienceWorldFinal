from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from ..db.sessions import get_db
from ..schemas.thread_schemas import ThreadRead, ThreadCreate
from ..services import thread_service

threads_router = APIRouter(prefix="/threads", tags=["Threads"])


@threads_router.post("/", response_model=ThreadRead)
async def create_thread(thread: ThreadCreate, db: AsyncSession = Depends(get_db)):
    return await thread_service.create_thread(db, thread)


@threads_router.get("/group/{group_id}", response_model=list[ThreadRead])
async def get_threads_by_group(group_id: UUID, db: AsyncSession = Depends(get_db)):
    return await thread_service.get_threads_by_group(db, group_id)


@threads_router.get("/{thread_id}", response_model=ThreadRead)
async def get_thread(thread_id: UUID, db: AsyncSession = Depends(get_db)):
    thread = await thread_service.get_thread(db, thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread
