import uuid
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
import logging

from .user_schemas import UserOut, UserIn, LoginResponse, LoginRequest, UserInUpdate
from .db.sessions import get_db
from .security.jwt_utils import create_access_token, verify_token
from .rabbit import rabbitmq_instance
from .user_service import create_user, authenticate_user, get_user, get_user_list, delete_user, update_user

user_router = APIRouter()

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.INFO)

@user_router.post('/register', response_model=UserOut)
async def register_user(user_in: UserIn, db: AsyncSession = Depends(get_db)):
    logger.info("Register start")
    user = await create_user(user_in, db)
    if not user:
        raise HTTPException(status_code=400, detail="User already registered")

    await rabbitmq_instance.send_broadcast("register_user",{
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
    })
    logger.info("Register end")
    return user

@user_router.post('/login', response_model=LoginResponse)
async def login_user(login_request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(login_request, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password")
    access_token = create_access_token({"sub": str(user.id)})
    return LoginResponse(token=access_token)

@user_router.get('/user/profile/{user_id}', response_model=UserOut)
async def get_user_rout(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    user = await get_user(user_id, db)
    return user

@user_router.post("/logout")
async def logout():
    return {"message": "Logout successful"}

@user_router.get('/user-list', response_model=List[UserOut])
async def get_user_list_rout(db: AsyncSession = Depends(get_db)):
    users = await get_user_list(db)
    return users

@user_router.delete('/user/delete/{user_id}')
async def delete_user_rout(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await delete_user(user_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    await rabbitmq_instance.send_broadcast("delete_user",{
        "id": user_id,
    })

    return result

@user_router.put('/user/update/{user_id}', response_model=UserOut)
async def update_user_rout(user_id: uuid.UUID, user_update_in: UserInUpdate, db: AsyncSession = Depends(get_db)):
    result = await update_user(user_id, user_update_in, db)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    await rabbitmq_instance.send_broadcast("update_user",{
        "id": user_id,
        "first_name": user_update_in.first_name,
        "last_name": user_update_in.last_name,
    })

    return result

@user_router.get("/user/check")
async def check_auth(user: dict = Depends(verify_token)):
    return {"isAuthenticated": True, "user": user}