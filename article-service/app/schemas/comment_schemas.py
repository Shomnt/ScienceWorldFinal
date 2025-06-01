import uuid

from pydantic import BaseModel


class CommentIn(BaseModel):
    content: str
    authir_id: uuid.UUID
    article_id: uuid.UUID

class CommentUpdateIn(BaseModel):
    content: str

class CommentOut(BaseModel):
    id: int
    content: str

    class Config:
        orm_mode = True
        from_attributes = True