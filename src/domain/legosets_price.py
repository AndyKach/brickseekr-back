from datetime import datetime
from pydantic import BaseModel, Field

class LegosetsPrice(BaseModel):
    legoset_id: str              = Field(default='')
    price: str                   = Field(default='-')
    website_id: str              = Field(default='0')
    created_at: datetime | str   = Field(default_factory=datetime.now)
