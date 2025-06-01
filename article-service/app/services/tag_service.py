from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..db.models import Tag
from ..schemas.tag_schemas import TagIn, TagOut


async def create_tag(tag_in: TagIn, db: AsyncSession) -> Tag:
    tag = await db.execute(select(Tag).where(Tag.name == tag_in.name))
    tag = tag.scalar_one_or_none()
    if tag is None:
        tag = Tag(name=tag_in.name)
        db.add(tag)
        await db.commit()
        await db.refresh(tag)
    return tag