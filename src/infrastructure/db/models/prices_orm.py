from datetime import datetime

from sqlalchemy import Column, String, JSON, INTEGER, Float, text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.db.base import Base

class LegoSetsPricesOrm(Base):
    __tablename__ = 'lego_sets_prices'

    price_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lego_set_id: Mapped[str] = mapped_column(String)
    prices: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

