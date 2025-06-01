from uuid import UUID

from pydantic import BaseModel, Field

class ThreadBase(BaseModel):
    title: str = Field(..., max_length=70)
    start_message: str = Field(..., max_length=400)

class ThreadCreate(ThreadBase):
    group_id: UUID

class ThreadRead(ThreadBase):
    id: UUID
    group_id: UUID