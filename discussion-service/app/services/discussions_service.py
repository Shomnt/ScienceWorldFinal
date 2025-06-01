import uuid

from sqlalchemy import select, func
from ..db.models import Group, GroupMember
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import models
from ..db.models import Group
from ..schemas.group_schemas import GroupCreate, GroupRead


async def get_list_discussions(db: AsyncSession):
    stmt = (
        select(
            Group.id,
            Group.title,
            Group.description,
            func.count(GroupMember.user_id).label("member_count")
        )
        .outerjoin(GroupMember, Group.id == GroupMember.group_id)
        .group_by(Group.id)
    )
    result = await db.execute(stmt)
    groups = result.all()

    # Конвертация в список GroupRead
    return [
        GroupRead(
            id=row.id,
            title=row.title,
            description=row.description,
            member_count=row.member_count,
        )
        for row in groups
    ]

async def create_group(db: AsyncSession, group: GroupCreate):
    db_group = models.Group(
        title=group.title,
        description=group.description,
    )
    db.add(db_group)
    await db.commit()
    await db.refresh(db_group)

    return GroupRead(
        id=db_group.id,
        title=db_group.title,
        description=db_group.description,
        member_count=0  # Только что созданная группа — участников нет
    )

async def get_group(db: AsyncSession, group_id: uuid.UUID):
    stmt = (
        select(
            Group.id,
            Group.title,
            Group.description,
            func.count(GroupMember.user_id).label("member_count"),
        )
        .outerjoin(GroupMember, Group.id == GroupMember.group_id)
        .where(Group.id == group_id)
        .group_by(Group.id)
    )
    result = await db.execute(stmt)
    row = result.one_or_none()
    if row is None:
        return None
    return GroupRead(
        id=row.id,
        title=row.title,
        description=row.description,
        member_count=row.member_count,
    )


async def get_group_by_title(db: AsyncSession, title: str):
    result = await db.execute(select(models.Group).where(models.Group.title == title))
    return result.scalar_one_or_none()