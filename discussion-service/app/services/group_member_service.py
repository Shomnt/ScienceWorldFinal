from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from ..db import models
from ..schemas.group_schemas import GroupMemberCreate


async def is_member(db: AsyncSession, group_id, user_id):
    result = await db.execute(
        select(models.GroupMember).where(
            models.GroupMember.group_id == group_id,
            models.GroupMember.user_id == user_id
        )
    )
    return result.scalar_one_or_none() is not None


async def add_member(db: AsyncSession, member: GroupMemberCreate):
    db_member = models.GroupMember(
        user_id=member.user_id,
        group_id=member.group_id,
    )
    db.add(db_member)
    await db.commit()


async def remove_member(db: AsyncSession, member: GroupMemberCreate):
    await db.execute(
        delete(models.GroupMember).where(
            models.GroupMember.group_id == member.group_id,
            models.GroupMember.user_id == member.user_id
        )
    )
    await db.commit()
