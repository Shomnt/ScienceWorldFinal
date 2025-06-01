import json
import uuid
from typing import List

from fastapi import APIRouter, Request, Depends, Form, UploadFile, File, HTTPException
from sqlalchemy import or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.sessions import get_db
from ..schemas.group_schemas import GroupRead, GroupCreate
from ..services import discussions_service

discussions_router = APIRouter(prefix="/groups", tags=["Groups"])


@discussions_router.post("/", response_model=GroupRead)
async def create_group(group: GroupCreate, db: AsyncSession = Depends(get_db)):
    db_group = await discussions_service.get_group_by_title(db, group.title)
    if db_group:
        raise HTTPException(status_code=400, detail="Group with this title already exists")
    return await discussions_service.create_group(db, group)


@discussions_router.get("/", response_model=list[GroupRead])
async def get_groups(db: AsyncSession = Depends(get_db)):
    return await discussions_service.get_list_discussions(db)


@discussions_router.get("/{group_id}", response_model=GroupRead)
async def get_group(group_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    group = await discussions_service.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


