from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from ..db.models import Area
from ..schemas.area_schemas import AreaIn, AreaOut


async def create_area(db: AsyncSession, area_in: AreaIn) -> AreaOut:
    area = Area(
        name=area_in.name,
        layer=area_in.layer,
    )

    db.add(area)
    await db.commit()
    await db.refresh(area)
    return area

async def get_area(db: AsyncSession, area_name: str) -> AreaOut:
    result = await db.execute(select(Area).where(Area.name == area_name))
    area = result.scalar_one_or_none()
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    return area

async def get_area_list(db: AsyncSession) -> List[AreaOut]:
    result = await db.execute(select(Area).order_by(Area.name))
    areas = result.scalars().all()
    if not areas:
        raise HTTPException(status_code=404, detail="Area not found")
    return areas

async def delete_area(db: AsyncSession, area_name: str) -> bool:
    result = await db.execute(select(Area).where(Area.name == area_name))
    area = result.scalar_one_or_none()
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    await db.delete(area)
    await db.commit()
    return True
