from datetime import datetime
from pydantic import BaseModel, Field

class LegoSetsPrice(BaseModel):
    lego_set_id: str = Field(default='')
    price: str = Field(default='')
    website_id: str = Field(default='')
    created_at: datetime = Field(default_factory=datetime.now)
