from datetime import datetime
from pydantic import BaseModel, Field

class LegoSetsPrices(BaseModel):
    lego_set_id: str = Field(default='')
    prices: dict = Field(default='')
    created_at: datetime = Field(default_factory=datetime.now)
