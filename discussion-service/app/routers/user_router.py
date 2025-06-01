import json
import uuid
from typing import List

from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from sqlalchemy import or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.sessions import get_db
from ..services.user_service import get_user_list

discussions_user_router = APIRouter()

@discussions_user_router.get("/users/list")
async def list_users(db: AsyncSession = Depends(get_db)):
    users = await get_user_list(db)
    return users
