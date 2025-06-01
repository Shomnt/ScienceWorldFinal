from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.sessions import get_db
from ..schemas.group_schemas import GroupMemberCreate
from ..services import group_member_service

group_member_router = APIRouter(prefix="/group-members", tags=["Group Membership"])


@group_member_router.post("/", status_code=201)
async def join_group(member: GroupMemberCreate, db: AsyncSession = Depends(get_db)):
    exists = await group_member_service.is_member(db, member.group_id, member.user_id)
    if exists:
        raise HTTPException(status_code=400, detail="User already in group")
    await group_member_service.add_member(db, member)
    return {"detail": "Joined group"}


@group_member_router.delete("/", status_code=204)
async def leave_group(member: GroupMemberCreate, db: AsyncSession = Depends(get_db)):
    exists = await group_member_service.is_member(db, member.group_id, member.user_id)
    if not exists:
        raise HTTPException(status_code=404, detail="User is not in group")
    await group_member_service.remove_member(db, member)
