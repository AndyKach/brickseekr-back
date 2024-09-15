from datetime import datetime
from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text


intpk = Annotated[int, mapped_column(primary_key=True)]

created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.utcnow,
)]
