from datetime import datetime
from pydantic import BaseModel, Field

class Minifigures(BaseModel):
    id: int = Field()
    name: str | None = Field(default='-')

    theme: str | None = Field(default='-')
    images: dict | None = Field(default={})

    updated_at: datetime | str | None = Field(default=None)
    created_at: datetime | str | None = Field(default_factory=datetime.now)
