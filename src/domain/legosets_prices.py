from datetime import datetime
from pydantic import BaseModel, Field

class LegosetsPrices(BaseModel):
    legoset_id: str              = Field(default='')
    prices: dict                 = Field(default='')
    created_at: datetime | str   = Field(default_factory=datetime.now)
