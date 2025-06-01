import uuid

from pydantic import BaseModel


class UserIn(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class UserInUpdate(BaseModel):
    first_name: str | None
    last_name: str | None
    email: str | None
    password: str | None

class UserOut(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    token: str
    token_type: str = 'bearer'