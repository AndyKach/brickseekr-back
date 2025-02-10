from datetime import datetime

from sqlalchemy import Column, String, JSON, INTEGER, Float, text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.db.base import Base


class LegoSetsOrm(Base):
    __tablename__ = "legosets"

    id: Mapped[str]                = mapped_column(String, primary_key=True)
    name: Mapped[str]              = mapped_column(String, default="-", nullable=True)
    year: Mapped[int]              = mapped_column(INTEGER, default=0, nullable=True)
    rating: Mapped[float]          = mapped_column(Float, default=0.0, nullable=True)

    theme: Mapped[str]             = mapped_column(String, default="-", nullable=True)
    themeGroup: Mapped[str]        = mapped_column(String, default="-", nullable=True)
    subtheme: Mapped[str]          = mapped_column(String, default="-", nullable=True)

    images: Mapped[dict]           = mapped_column(JSON, default={}, nullable=True)
    pieces: Mapped[int]            = mapped_column(INTEGER, default=0, nullable=True)
    dimensions: Mapped[dict]       = mapped_column(JSON, default={}, nullable=True)
    weigh: Mapped[float]           = mapped_column(Float, default=0.0, nullable=True)
    tags: Mapped[list]             = mapped_column(JSON, default=[], nullable=True)
    description: Mapped[str]       = mapped_column(String, default="-", nullable=True)
    ages_range: Mapped[dict]       = mapped_column(JSON, default={}, nullable=True)

    minifigures_ids: Mapped[list]  = mapped_column(JSON, default=[], nullable=True)
    minifigures_count: Mapped[int] = mapped_column(INTEGER, default=0, nullable=True)

    extendedData: Mapped[dict]     = mapped_column(JSON, default={'cz_url_name': "None", 'cz_category_name': "None"}, nullable=True)

    launchDate: Mapped[datetime]   = mapped_column(nullable=True)
    exitDate: Mapped[datetime]     = mapped_column(nullable=True)
    updated_at: Mapped[datetime]   = mapped_column(nullable=True)
    created_at: Mapped[datetime]   = mapped_column(server_default=text("TIMEZONE('utc', now())"))
