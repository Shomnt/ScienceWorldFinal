from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from ..db import models
from ..schemas.comment_schemas import CommentCreate


async def create_comment(db: AsyncSession, comment: CommentCreate):
    db_comment = models.Comment(
        thread_id=comment.thread_id,
        user_id=comment.user_id,
        content=comment.content,
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment


async def get_comments_by_thread(db: AsyncSession, thread_id: UUID):
    result = await db.execute(select(models.Comment).where(models.Comment.thread_id == thread_id))
    return result.scalars().all()
