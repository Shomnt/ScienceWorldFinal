import uuid
from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

#################
# Single Models #
#################

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(String(70), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String(70), unique=False, nullable=False)

    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="user")

    group_members: Mapped[List["GroupMember"]] = relationship("GroupMember", back_populates="user")

class Group(Base):
    __tablename__ = "groups"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(70), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)

    threads: Mapped[List["Thread"]] = relationship("Thread", back_populates="group")

    group_members: Mapped[List["GroupMember"]] = relationship("GroupMember", back_populates="group")


class Thread(Base):
    __tablename__ = "threads"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(70), unique=False, nullable=False)
    start_message: Mapped[str] = mapped_column(String(400), unique=False, nullable=False)

    group_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE", onupdate="CASCADE"))
    group: Mapped[Group] = relationship("Group", back_populates="threads")

    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="thread")

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content: Mapped[str] = mapped_column(String(400), unique=False, nullable=False)

    thread_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("threads.id", ondelete="CASCADE"))
    thread: Mapped[Thread] = relationship("Thread", back_populates="comments")

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship("User", back_populates="comments")

#######################
# Many To Many models #
#######################

class GroupMember(Base):
    __tablename__ = "group_members"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True, nullable=False)
    group_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("groups.id"), primary_key=True, nullable=False)

    user: Mapped[User] = relationship("User", back_populates="group_members")
    group: Mapped[Group] = relationship("Group", back_populates="group_members")