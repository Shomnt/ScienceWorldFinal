from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from ..db import models
from ..schemas.thread_schemas import ThreadCreate


async def create_thread(db: AsyncSession, thread: ThreadCreate):
    db_thread = models.Thread(
        title=thread.title,
        start_message=thread.start_message,
        group_id=thread.group_id,
    )
    db.add(db_thread)
    await db.commit()
    await db.refresh(db_thread)
    return db_thread


async def get_thread(db: AsyncSession, thread_id: UUID):
    result = await db.execute(select(models.Thread).where(models.Thread.id == thread_id))
    return result.scalar_one_or_none()


async def get_threads_by_group(db: AsyncSession, group_id: UUID):
    result = await db.execute(select(models.Thread).where(models.Thread.group_id == group_id))
    return result.scalars().all()
