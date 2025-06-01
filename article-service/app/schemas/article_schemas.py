import uuid
from typing import List

from pydantic import BaseModel


class ArticleIn(BaseModel):
    title: str
    description: str
    authors: List[str]
    tags: List[str]
    areas: List[str]

class ArticleOut(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    authors: List[str]
    tags: List[str]
    areas: List[str]
    file_path: str

    class Config:
        orm_mode = True
        from_attributes = True

class ArticleUpdateIn(BaseModel):
    title: str | None
    description: str | None
    authors: List[str] | None
    tags: List[str] | None
    areas: List[str] | None


