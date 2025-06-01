import uuid

from pydantic import BaseModel


class AuthorIn(BaseModel):
    id: str
    first_name: str
    last_name: str


class AuthorOut(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    rating: float

    class Config:
        orm_mode = True
        from_attributes = True

class AuthorUpdateIn(BaseModel):
    first_name: str | None
    last_name: str | None