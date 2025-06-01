import uuid
from typing import List

from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from .user_schemas import UserIn, UserOut, LoginRequest, UserInUpdate
from .db.models import User
from .security.hash_functions import hash_password, verify_password


async def create_user(user_in: UserIn, db: AsyncSession) -> UserOut:
    result = await db.execute(select(User).where(User.email == user_in.email))
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        hash_password=hash_password(user_in.password),
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def update_user(user_id: uuid.UUID, user_in: UserInUpdate, db: AsyncSession) -> UserOut:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_in.first_name is not None:
        user.first_name = user_in.first_name
    if user_in.last_name is not None:
        user.last_name = user_in.last_name
    if user_in.email is not None:
        result = await db.execute(select(User).where(User.email == user_in.email))
        test_user = result.scalar_one_or_none()
        if test_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        user.email = user_in.email
    if user_in.password is not None:
        user.hash_password = hash_password(user_in.password)

    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(user_id: uuid.UUID, db: AsyncSession) -> bool:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return True

async def get_user(user_id: uuid.UUID, db: AsyncSession) -> UserOut:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

async def get_user_list(db: AsyncSession) -> List[UserOut]:
    result = await db.execute(select(User).order_by(User.last_name, User.first_name))
    users = result.scalars().all()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return users

async def authenticate_user(login_request: LoginRequest, db: AsyncSession) -> UserOut | bool:
    result = await db.execute(select(User).where(User.email == login_request.email))
    user = result.scalar_one_or_none()
    if not user:
        return False
    if not verify_password(login_request.password, user.hash_password):
        return False

    return user

async def check_user(user_id: uuid.UUID, db: AsyncSession) -> bool:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return False
    return True