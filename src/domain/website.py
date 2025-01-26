from datetime import datetime
from pydantic import BaseModel, Field

class Website(BaseModel):
    id: int = Field()
    name: str = Field(default='-')
    created_at: datetime | str | None = Field(default_factory=datetime.now)