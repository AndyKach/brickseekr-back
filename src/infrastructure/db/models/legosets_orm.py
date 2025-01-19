from datetime import datetime

from sqlalchemy import Column, String, JSON, INTEGER, Float, text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.db.base import Base


class LegoSetsOrm(Base):
    __tablename__ = "legosets"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, default="-")
    year: Mapped[int] = mapped_column(INTEGER, default=0)

    theme: Mapped[str] = mapped_column(String, default="-")
    themeGroup: Mapped[str] = mapped_column(String, default="-")
    subtheme: Mapped[str] = mapped_column(String, default="-")

    images: Mapped[dict] = mapped_column(JSON, default={})
    pieces: Mapped[int] = mapped_column(String, default=0)
    dimensions: Mapped[dict] = mapped_column(JSON, default={})
    weigh: Mapped[float] = mapped_column(Float, default=0.0)
    tags: Mapped[list] = mapped_column(JSON, default=[])
    description: Mapped[str] = mapped_column(String, default="-")
    ages_range: Mapped[dict] = mapped_column(JSON, default={})

    extendedData: Mapped[dict] = mapped_column(JSON, default={'cz_url_name': "None", 'cz_category_name': "None"})

    launchDate: Mapped[datetime] = mapped_column(nullable=True)
    exitDate: Mapped[datetime] = mapped_column(nullable=True)
    updated_at: Mapped[datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
