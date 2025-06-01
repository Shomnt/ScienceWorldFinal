import uuid

from pydantic import BaseModel


class AreaIn(BaseModel):
    name: str
    layer: str

class AreaOut(BaseModel):
    id: uuid.UUID
    name: str
    layer: str

    class Config:
        orm_mode = True
        from_attributes = True