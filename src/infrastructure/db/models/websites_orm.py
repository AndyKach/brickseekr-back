from datetime import datetime

from sqlalchemy import Column, String, JSON, INTEGER, Float, text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.db.base import Base


class WebsitesOrm(Base):
    __tablename__ = "websites"

    id: Mapped[int]                = mapped_column(Integer, primary_key=True)
    name: Mapped[str]              = mapped_column(String, nullable=False)
    link: Mapped[str]              = mapped_column(String, nullable=True)
    created_at: Mapped[datetime]   = mapped_column(server_default=text("TIMEZONE('utc', now())"))

