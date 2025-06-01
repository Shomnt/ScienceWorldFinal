import json
import logging
import os
import shutil
import uuid
from typing import List

from fastapi import Form, File, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload

from .author_service import change_rating
from ..db.models import Article, Author, AuthorArticle, ArticleTag, Area, ArticleArea, ArticleReference, Tag
from ..hash_functions import hash_file
from ..schemas.article_schemas import ArticleOut
from ..schemas.tag_schemas import TagIn
from ..services import tag_service

UPLOAD_DIR = "../uploads"

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.INFO)

async def create_article(
    db: AsyncSession,
    title: str = Form(...),
    description: str = Form(...),
    authors: str = Form(...),
    tags: str = Form(...),
    areas: str = Form(...),
    file: UploadFile = File(...)
) -> ArticleOut:

    file_hash = hash_file(file.file)
    result = await db.execute(select(Article).where(Article.file_hash == file_hash))
    if result.scalar():
        raise HTTPException(status_code=400, detail="This article has already been uploaded")

    article = Article(title=title, description=description, file_hash=file_hash)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    _, ext = os.path.splitext(file.filename)
    logger.info(f".{ext}")
    new_filename = f"{uuid.uuid4().hex}{ext}"
    logger.info(f"New file name is {new_filename}")
    file_path = os.path.join(UPLOAD_DIR, new_filename)
    logger.info(f"File path is {file_path}")
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    article.file_path = file_path

    db.add(article)

    author_ids = json.loads(authors)
    tag_names = json.loads(tags)
    area_names = json.loads(areas)

    if author_ids:
        result = await db.execute(select(Author).where(Author.id.in_(author_ids)))
        for author in result.scalars():
            db.add(AuthorArticle(author=author, article=article))

    for tag_name in tag_names:
        tag = await tag_service.create_tag(TagIn(name=tag_name), db)
        db.add(ArticleTag(article=article, tag=tag))

    if area_names:
        result = await db.execute(select(Area).where(Area.name.in_(area_names)))
        for area in result.scalars():
            db.add(ArticleArea(article=article, area=area))


    await db.commit()

    stmt = select(Article).options(
        selectinload(Article.authors_articles).selectinload(AuthorArticle.author),
        selectinload(Article.article_tags).selectinload(ArticleTag.tag),
        selectinload(Article.article_areas).selectinload(ArticleArea.area),
    ).where(Article.id == article.id)

    result = await db.execute(stmt)
    return result.scalar_one()

async def get_article(db: AsyncSession, id: uuid.UUID) -> ArticleOut:
    result = await db.execute(select(Article).where(Article.id == id))
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

async def get_article_object(db: AsyncSession, id: uuid.UUID) -> Article:
    result = await db.execute(
        select(Article)
        .options(
            selectinload(Article.authors_articles).selectinload(AuthorArticle.author),
            selectinload(Article.article_tags).selectinload(ArticleTag.tag),
            selectinload(Article.article_areas).selectinload(ArticleArea.area),
        )
        .where(Article.id == id))
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

async def delete_article(db: AsyncSession, id: uuid.UUID) -> bool:
    result = await db.execute(select(Article).where(Article.id == id))
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    await db.delete(article)
    await db.commit()
    return True

async def update_article(
    db: AsyncSession,
    id: uuid.UUID = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    authors: str = Form(...),
    tags: str = Form(...),
    areas: str = Form(...),
    file: UploadFile = File(None),
) -> ArticleOut:

    result = await db.execute(select(Article).where(Article.id == id))
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if file:
        file_hash = hash_file(file.file)
        existing = await db.execute(select(Article).where(Article.file_hash == file_hash, Article.id != article.id))
        if existing.scalar():
            raise HTTPException(status_code=400, detail="This article has already been uploaded")
        article.file_hash = file_hash

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        _, ext = os.path.splitext(file.filename)
        new_filename = uuid.uuid4().hex + ext
        file_location = os.path.join(UPLOAD_DIR, new_filename)
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        article.file_path = file_location

    article.title = title
    article.description = description

    author_ids = json.loads(authors)
    tag_names = json.loads(tags)
    area_names = json.loads(areas)

    if author_ids:
        result = await db.execute(select(Author).where(Author.id.in_(author_ids)))
        authors_list = result.scalars().all()
        existing_links = {(aa.author_id, aa.article_id) async for aa in await db.stream(
            select(AuthorArticle).where(AuthorArticle.article_id == article.id)
        )}
        for author in authors_list:
            if (author.id, article.id) not in existing_links:
                db.add(AuthorArticle(author_id=author.id, article_id=article.id))

    if tag_names:
        existing_tags = {(at.tag_id, at.article_id) async for at in await db.stream(
            select(ArticleTag).where(ArticleTag.article_id == article.id)
        )}
        for tag_name in tag_names:
            tag = await tag_service.create_tag(TagIn(name=tag_name), db)
            if (tag.id, article.id) not in existing_tags:
                db.add(ArticleTag(tag_id=tag.id, article_id=article.id))

    if area_names:
        result = await db.execute(select(Area).where(Area.name.in_(area_names)))
        areas_list = result.scalars().all()
        existing_areas = {(aa.area_id, aa.article_id) async for aa in await db.stream(
            select(ArticleArea).where(ArticleArea.article_id == article.id)
        )}
        for area in areas_list:
            if (area.id, article.id) not in existing_areas:
                db.add(ArticleArea(area_id=area.id, article_id=article.id))

    await db.commit()

    stmt = select(Article).options(
        selectinload(Article.authors_articles).selectinload(AuthorArticle.author),
        selectinload(Article.article_tags).selectinload(ArticleTag.tag),
        selectinload(Article.article_areas).selectinload(ArticleArea.area),
    ).where(Article.id == article.id)

    result = await db.execute(stmt)
    return result.scalar_one()

async def get_article_list(db: AsyncSession) -> List[ArticleOut]:
    result = await db.execute(select(Article).order_by(Article.title))
    articles = result.scalars().all()
    if not articles:
        raise HTTPException(status_code=404, detail="Article not found")
    return articles


async def update_article_rating(article: Article, new_rating: float, layer: int, db: AsyncSession):
    if layer >= 5:
        return

    article.rating = article.rating + new_rating
    await db.commit()
    await db.refresh(article)

    for authors_articles in article.authors_articles:
        await change_rating(db, authors_articles.author)

    result = await db.execute(
        select(Article).join(ArticleReference, Article.id == ArticleReference.article_id)
        .where(ArticleReference.reference_id == article.id)
    )
    referencing_articles = result.scalars().all()

    for ref_article in referencing_articles:
        await update_article_rating(ref_article, new_rating*0.1, layer+1, db)

async def calculate_new_rating(article: Article, mark: int, factor: float, db: AsyncSession):
    new_rating = (1/(10^(11-mark)))*factor
    await update_article_rating(article=article, new_rating=new_rating, layer=1, db=db)


from sqlalchemy import or_, desc


async def search_articles(db: AsyncSession, query: str) -> List[ArticleOut]:
    stmt = select(Article).where(
        or_(
            Article.title.ilike(f"%{query}%"),
            Article.description.ilike(f"%{query}%")
        )
    ).order_by(Article.title)

    result = await db.execute(stmt)
    return result.scalars().all()

async def filter_articles(db: AsyncSession, tag_names: list[str], area_names: list[str]) -> List[ArticleOut]:
    stmt = select(Article).distinct().options(
        joinedload(Article.article_tags).joinedload(ArticleTag.tag),
        joinedload(Article.article_areas).joinedload(ArticleArea.area),
    )

    if tag_names:
        stmt = stmt.join(ArticleTag).join(Tag).where(Tag.name.in_(tag_names))

    if area_names:
        stmt = stmt.join(ArticleArea).join(Area).where(Area.name.in_(area_names))

    result = await db.execute(stmt)
    return result.scalars().all()

async def sort_articles(db: AsyncSession, sort_by: str) -> List[ArticleOut]:
    if sort_by == "title":
        stmt = select(Article).order_by(Article.title)
    elif sort_by == "rating":
        stmt = select(Article).order_by(desc(Article.rating))
    else:
        stmt = select(Article).order_by(Article.title)

    result = await db.execute(stmt)
    return result.scalars().all()
