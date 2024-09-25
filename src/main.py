import asyncio

from infrastructure.db.base import Base, sync_engine, async_engine
from infrastructure.config.fastapi_app_config import app
import infrastructure.web.api


# async def init_models():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)

if __name__ == '__main__':
    # asyncio.run(init_models())
    pass
