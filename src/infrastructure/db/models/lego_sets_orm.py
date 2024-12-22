from datetime import datetime

from sqlalchemy import Column, String, JSON, INTEGER, Float, text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.db.base import Base


class LegoSetsOrm(Base):
    __tablename__ = "lego_sets"

    lego_set_id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, default="-")
    category_name: Mapped[str] = mapped_column(String, default="0")
    year: Mapped[int] = mapped_column(INTEGER, default=0)
    weigh: Mapped[float] = mapped_column(Float, default=0.0)
    dimensions: Mapped[dict] = mapped_column(JSON, default={})
    ages: Mapped[int] = mapped_column(INTEGER, default=0)
    images: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
