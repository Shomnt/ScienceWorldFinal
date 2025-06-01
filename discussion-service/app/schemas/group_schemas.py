from uuid import UUID

from pydantic import BaseModel, Field


class GroupBase(BaseModel):
    title: str = Field(..., max_length=70)
    description: str = Field(..., max_length=200)

class GroupCreate(GroupBase):
    pass

class GroupRead(GroupBase):
    id: UUID
    member_count: int

    class Config:
        orm_mode = True

class GroupMemberCreate(BaseModel):
    group_id: UUID
    user_id: UUID