import json
import uuid
from typing import List, Optional

from fastapi import APIRouter, Request, Depends, Form, UploadFile, File, HTTPException, Query
from sqlalchemy import or_, desc
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import Author, Tag, Area, Article, ArticleTag, ArticleArea, AuthorArticle
from ..db.sessions import get_db
from ..rabbit import send_rpc_request
from ..schemas.area_schemas import AreaIn, AreaOut
from ..schemas.article_schemas import ArticleOut
from ..schemas.author_schemas import AuthorOut
from ..security import get_current_user
from ..services.article_service import get_article_object, calculate_new_rating, get_article_list, create_article, \
    get_article
from ..services.author_service import get_author_object
from ..services.area_service import create_area
from ..services import author_service

article_router = APIRouter()

@article_router.post("/rating/{article_id}/{mark}")
async def rate_article(article_id: uuid.UUID, mark: int, request: Request, db: AsyncSession = Depends(get_db)):
    payload = await get_current_user(request)
    user_id = payload["sub"]
    user = await get_author_object(db, user_id)
    article = await get_article_object(db, article_id)

    response = await send_rpc_request({
        "user_area_list": user.areas,
        "article_area_list": article.areas,
        "user_rating": user.rating,
    })

    await calculate_new_rating(article, mark, response["addition_rating"], db)

    return json.dump({
        "message": "success",
    })

@article_router.get("/author/{author_id}", response_model=AuthorOut)
async def get_author(author_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    author = await author_service.get_author(db, author_id)
    return author

@article_router.get("/authors", response_model=List[AuthorOut])
async def get_authors_list(db: AsyncSession = Depends(get_db)):
    authors = await db.execute(select(Author))
    authors_list = authors.scalars().all()
    return authors_list

from sqlalchemy.orm import selectinload
from sqlalchemy import or_, desc
from fastapi import Depends, Query
from typing import List, Optional

@article_router.get("/articles", response_model=List[ArticleOut])
async def get_articles(
    db: AsyncSession = Depends(get_db),
    query: Optional[str] = None,
    tags: List[str] = Query(default=[]),
    areas: List[str] = Query(default=[]),
    sort_by: Optional[str] = "title"
):
    stmt = select(Article).distinct().options(
        selectinload(Article.authors_articles).selectinload(AuthorArticle.author),
        selectinload(Article.article_tags).selectinload(ArticleTag.tag),
        selectinload(Article.article_areas).selectinload(ArticleArea.area),
    )

    if tags:
        stmt = stmt.join(ArticleTag).join(Tag).where(Tag.name.in_(tags))

    if areas:
        stmt = stmt.join(ArticleArea).join(Area).where(Area.name.in_(areas))

    if query:
        stmt = stmt.where(
            or_(
                Article.title.ilike(f"%{query}%"),
                Article.description.ilike(f"%{query}%")
            )
        )

    if sort_by == "rating":
        stmt = stmt.order_by(desc(Article.rating))
    else:
        stmt = stmt.order_by(Article.title)

    result = await db.execute(stmt)
    articles = result.scalars().unique().all()  # .unique() на случай джойнов

    # Возвращаем Pydantic модели из ORM объектов
    return [ArticleOut.from_orm(article) for article in articles]

@article_router.post("/article/upload", response_model=ArticleOut)
async def create_article_route(
        title: str = Form(...),
        description: str = Form(...),
        authors: str = Form(...),
        tags: str = Form(...),
        areas: str = Form(...),
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db)):
    return await create_article(
        db=db,
        title=title,
        description=description,
        authors=authors,
        tags=tags,
        areas=areas,
        file=file
    )

@article_router.get("/authors/clue")
async def get_authors(query: str = "", db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Author).where(
        or_(
            Author.first_name.ilike(f"%{query}%"),
            Author.last_name.ilike(f"%{query}%")
        )
    ))
    authors = result.scalars().all()
    return [{"id": a.id, "name": a.full_name} for a in authors]

@article_router.get("/tags/clue")
async def get_tags(query: str = "", db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag).where(Tag.name.ilike(f"%{query}%")))
    tags = result.scalars().all()
    return [{"id": t.id, "name": t.name} for t in tags]

@article_router.get("/areas/clue")
async def get_areas(query: str = "", db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Area).where(Area.name.ilike(f"%{query}%")).where(Area.layer == "second"))
    areas = result.scalars().all()
    return [{"id": a.id, "name": a.name} for a in areas]

@article_router.post("/area/create", response_model=AreaOut)
async def area_create(area_in: AreaIn, db: AsyncSession = Depends(get_db)):
    result = await create_area(db, area_in)
    return result

@article_router.get("/articles/{article_id}")
async def get_article_by_id(article_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    article = await get_article_object(db, article_id)
    return article