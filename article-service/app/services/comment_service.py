import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from ..db.models import Comment
from ..schemas.comment_schemas import CommentIn, CommentOut, CommentUpdateIn


async def create_comment(db: AsyncSession, comment_in: CommentIn) -> CommentOut:
    comment = Comment(
        text=comment_in.content,
        author_id=comment_in.author_id,
        article_id=comment_in.article_id,
    )

    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment

async def get_comment(db: AsyncSession, comment_id: uuid.UUID) -> CommentOut:
    comment = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = comment.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

async def update_comment(db: AsyncSession, comment_id: uuid.UUID, comment_update_in: CommentUpdateIn) -> CommentOut:
    comment = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = comment.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    comment.text = comment_update_in.content
    await db.commit()
    await db.refresh(comment)
    return comment

async def delete_comment(db: AsyncSession, comment_id: uuid.UUID) -> bool:
    comment = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = comment.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    await db.delete(comment)
    await db.commit()
    return True