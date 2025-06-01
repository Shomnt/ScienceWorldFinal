from pydantic import BaseModel


class UserIn(BaseModel):
    id: str
    first_name: str
    last_name: str

class UserUpdateIn(BaseModel):
    id: str
    first_name: str
    last_name: str
