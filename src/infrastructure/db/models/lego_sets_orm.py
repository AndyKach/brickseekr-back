from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.db.base import Base
from infrastructure.db.models.orm_template_columns import intpk, created_at


class LegoSetsOrm(Base):
    __tablename__ = "lego_sets"

    set_id: str = Mapped[str]
    images: dict = Mapped[dict]
    name: str = Mapped[str]
    year: str = Mapped[str]
    weigh: float = Mapped[float]
    dimensions: dict | None = Mapped[dict]
    ages: int = Mapped[int]
    created_at: Mapped[created_at]
