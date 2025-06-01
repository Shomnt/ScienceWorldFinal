import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(String(70), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String(70), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hash_password: Mapped[str] = mapped_column(String(400), unique=False, nullable=False)
    role: Mapped[str] = mapped_column(String(50), unique=False, nullable=False, default='base')