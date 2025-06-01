import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.future import select

from ..db.models import User
from ..schemas.user_schemas import UserIn, UserUpdateIn


async def create_user(db: AsyncSession, user_in: UserIn):
    user_id = uuid.UUID(user_in.id)
    user = User(
        id=user_id,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
    )

    db.add(user)
    await db.commit()
    return user

async def update_user(db: AsyncSession, user_in: UserUpdateIn):
    user = await db.execute(select(User).where(User.id == user_in.id))
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_in.first_name:
        user.first_name = user_in.first_name
    if user_in.last_name:
        user.last_name = user_in.last_name
    await db.commit()
    return user

async def delete_user(db: AsyncSession, user_id: uuid.UUID):
    user = await db.execute(select(User).where(User.id == user_id))
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return True

async def get_user_list(db: AsyncSession):
    users = await db.execute(select(User).order_by(User.id))
    users = users.scalars().all()
    return users