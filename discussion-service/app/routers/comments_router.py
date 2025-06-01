from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from ..db.sessions import get_db
from ..schemas.comment_schemas import CommentRead, CommentCreate
from ..services import comment_service

comment_router = APIRouter(prefix="/comments", tags=["Comments"])


@comment_router.post("/", response_model=CommentRead)
async def create_comment(comment: CommentCreate, db: AsyncSession = Depends(get_db)):
    return await comment_service.create_comment(db, comment)


@comment_router.get("/thread/{thread_id}", response_model=list[CommentRead])
async def get_comments_by_thread(thread_id: UUID, db: AsyncSession = Depends(get_db)):
    return await comment_service.get_comments_by_thread(db, thread_id)
