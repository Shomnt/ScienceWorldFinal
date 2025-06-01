import uuid

from pydantic import BaseModel


class TagIn(BaseModel):
    name: str

class TagOut(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        orm_mode = True
        from_attributes = True