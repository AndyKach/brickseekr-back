from datetime import datetime

from sqlalchemy import Column, String, JSON, INTEGER, Float, text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.db.base import Base

class LegoSetsPricesOrm(Base):
    __tablename__ = 'legosets_prices'

    legoset_id: Mapped[str] = mapped_column(String, primary_key=True)
    prices: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

