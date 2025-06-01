import uuid
from typing import List

from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

#################
# Single Models #
#################

class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(70), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String(70), unique=False, nullable=False)

    rating: Mapped[float] = mapped_column(Float, unique=False, nullable=False, default=1)

    authors_articles: Mapped[List["AuthorArticle"]] = relationship("AuthorArticle", back_populates="author")
    authors_areas: Mapped[List["AuthorArea"]] = relationship("AuthorArea", back_populates="author")

    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="author")

    @property
    def articles(self):
        return sorted(aa.article.title for aa in self.authors_articles)

    @property
    def areas(self):
        return sorted(aa.area.name for aa in self.authors_areas)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Article(Base):
    __tablename__ = 'articles'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    description: Mapped[str] = mapped_column(String(300), unique=False, nullable=False)
    rating: Mapped[float] = mapped_column(Float, unique=False, nullable=False, default=0)

    file_path: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    file_hash: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    authors_articles: Mapped[List["AuthorArticle"]] = relationship("AuthorArticle", back_populates="article")

    article_tags: Mapped[list["ArticleTag"]] = relationship("ArticleTag", back_populates="article")
    article_areas: Mapped[list["ArticleArea"]] = relationship("ArticleArea", back_populates="article")

    article_reference = relationship("ArticleReference", foreign_keys="[ArticleReference.article_id]" ,back_populates="article",
                                      cascade="save-update, merge, refresh-expire")
    referenced_by = relationship("ArticleReference", foreign_keys="[ArticleReference.reference_id]", back_populates="reference",
                                      cascade="save-update, merge, refresh-expire")

    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="article")

    @property
    def tags(self):
        return sorted([at.tag.name for at in self.article_tags])

    @property
    def areas(self):
        return sorted([aa.area.name for aa in self.article_areas])

    @property
    def authors(self):
        return sorted([f"{aa.author.first_name} {aa.author.last_name}" for aa in self.authors_articles])

    @property
    def references(self):
        return sorted([ar.reference.title for ar in self.article_reference])

    @property
    def reference_by_who(self):
        return sorted([rb.article.title for rb in self.referenced_by])

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    article_tags: Mapped[list["ArticleTag"]] = relationship("ArticleTag", back_populates="tag")

    @property
    def articles(self):
        return sorted([at.article.title for at in self.article_tags])

class Area(Base):
    __tablename__ = "areas"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    layer: Mapped[str] = mapped_column(String(100), nullable=False)
    article_areas: Mapped[List["ArticleArea"]] = relationship("ArticleArea", back_populates="area")
    authors_areas: Mapped[List["AuthorArea"]] = relationship("AuthorArea", back_populates="area")

    @property
    def articles(self):
        return sorted([aa.article.title for aa in self.article_areas])

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text: Mapped[str] = mapped_column(String(700), nullable=False)

    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))
    article_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("articles.id", ondelete="CASCADE"))

    author: Mapped[Author] = relationship("Author", back_populates="comments")
    article: Mapped[Article] = relationship("Article", back_populates="comments")


#######################
# Many To Many models #
#######################

class AuthorArticle(Base):
    __tablename__ = 'author_articles'

    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("authors.id"), primary_key=True, nullable=False)
    article_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("articles.id"), primary_key=True, nullable=False)

    author: Mapped[Author] = relationship("Author", back_populates="authors_articles")
    article: Mapped[Article] = relationship("Article", back_populates="authors_articles")

class ArticleTag(Base):
    __tablename__ = "article_tags"

    article_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("articles.id"), primary_key=True, nullable=False)
    tag_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tags.id"), primary_key=True, nullable=False)

    article: Mapped["Article"] = relationship("Article", back_populates="article_tags")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="article_tags")

class ArticleArea(Base):
    __tablename__ = "article_areas"

    area_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("areas.id"), primary_key=True, nullable=False)
    article_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("articles.id"), primary_key=True, nullable=False)

    area: Mapped["Area"] = relationship("Area", back_populates="article_areas")
    article: Mapped["Article"] = relationship("Article",back_populates="article_areas")

class ArticleReference(Base):
    __tablename__ = "article_references"

    article_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("articles.id"), primary_key=True, nullable=False)
    reference_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("articles.id"), primary_key=True, nullable=False)

    article: Mapped["Article"] = relationship("Article", foreign_keys=[article_id], back_populates="article_reference")
    reference: Mapped["Article"] = relationship("Article", foreign_keys=[reference_id], back_populates="referenced_by")

class AuthorArea(Base):
    __tablename__ = "author_areas"

    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("authors.id"), primary_key=True, nullable=False)
    area_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("areas.id"), primary_key=True, nullable=False)

    author: Mapped["Author"] = relationship("Author", back_populates="authors_areas")
    area: Mapped["Area"] = relationship("Area", back_populates="authors_areas")
