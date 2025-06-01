from uuid import UUID

from pydantic import BaseModel, Field

class CommentBase(BaseModel):
    content: str = Field(..., max_length=400)

class CommentCreate(CommentBase):
    thread_id: UUID
    user_id: UUID

class CommentRead(CommentBase):
    id: UUID
    thread_id: UUID
    user_id: UUID