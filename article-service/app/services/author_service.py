import logging
import math
import uuid
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.future import select

from ..db.models import Author
from ..schemas.author_schemas import AuthorIn, AuthorOut, AuthorUpdateIn

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.INFO)

async def create_author(db: AsyncSession, author_in: AuthorIn) -> AuthorOut:
    logger.info("Start create author")
    logger.info(f"Trying to parse UUID from: {author_in.id}")
    author_id = uuid.UUID(author_in.id)
    logger.info(f"UUID parsed: {author_id}")
    author = Author(
        id=author_id,
        first_name=author_in.first_name,
        last_name=author_in.last_name,
    )
    logger.info("Model was created successfully")
    db.add(author)
    logger.info("Model was add successfully")
    await db.commit()
    logger.info("Model was commit successfully")
    logger.info("End create author")
    return AuthorOut(
        id=author.id,
        first_name=author.first_name,
        last_name=author.last_name,
        rating=author.rating,
    )

async def get_author(db: AsyncSession, author_id: uuid.UUID) -> AuthorOut:
    author = await db.execute(select(Author).where(Author.id == author_id))
    author = author.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

async def get_author_object(db: AsyncSession, author_id: uuid.UUID) -> Author:
    author = await db.execute(select(Author).where(Author.id == author_id))
    author = author.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

async def get_author_list(db: AsyncSession) -> List[AuthorOut]:
    authors = await db.execute(select(Author).order_by(Author.first_name))
    authors = authors.scalars().all()
    if not authors:
        raise HTTPException(status_code=404, detail="Author not found")
    return authors

async def update_author(db: AsyncSession, author_id: uuid.UUID, author_update_in: AuthorUpdateIn) -> AuthorOut:
    author = await db.execute(select(Author).where(Author.id == author_id))
    author = author.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    if author_update_in.first_name:
        author.first_name = author_update_in.first_name
    if author_update_in.last_name:
        author.last_name = author_update_in.last_name
    await db.commit()
    await db.refresh(author)
    return author

async def delete_author(db: AsyncSession, author_id: uuid.UUID) -> bool:
    author = await db.execute(select(Author).where(Author.id == author_id))
    author = author.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    await db.delete(author)
    await db.commit()
    return True

async def change_rating(db: AsyncSession, author: Author) -> bool:
    rating = 0.0
    for author_article in author.authors_articles:
        rating += author_article.article.rating
    author.rating = 11*math.log(rating+1)
    await db.commit()
    await db.refresh(author)
    return True