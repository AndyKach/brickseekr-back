from datetime import datetime
from pydantic import BaseModel, Field


class LegoSet(BaseModel):
    lego_set_id: str = Field(default='')
    images: dict = Field(default={})
    name: str = Field(default='')
    year: int = Field(default='')
    weigh: float = Field(default='')
    dimensions: dict | None = Field(default={})
    ages: int = Field(default=0)
    created_at: datetime | None = Field(default_factory=datetime.now)


"""

lego_set_id=,
images=,
name=,
year=,
weigh=,
dimensions=,
ages=,
created_at=,

"""

