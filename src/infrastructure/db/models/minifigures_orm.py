from datetime import  datetime
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, JSON, text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.db.base import Base

class MinifiguresOrm(Base):
    __tablename__ = "minifigures"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=True)

    theme: Mapped[str] = mapped_column(String, nullable=True)
    images: Mapped[list] = mapped_column(JSON, nullable=True)

    updated_at: Mapped[datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
