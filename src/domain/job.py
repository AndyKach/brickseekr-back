from datetime import datetime
from typing import List
from typing import Optional, Callable
from pydantic import BaseModel, Field


class Job(BaseModel):
    func: Callable = Field(default=None)
    trigger: str = Field(default=None)
    run_date: datetime = Field(default=None)
    hour: int | None = Field(default=None)
    minute: int | None = Field(default=None)
    day_of_week: str | None = Field(default=None)
    args: list = Field(default=None)
    id: Optional[str] = Field(default=None)
    job_type: Optional[str] = Field(default=None)


