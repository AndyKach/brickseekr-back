import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager
from infrastructure.config import logs_config
# from infrastructure.config.services_config import get_scheduler_service
from infrastructure.db.base import Base, sync_engine, async_engine

from infrastructure.web.api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # scheduler_service = get_scheduler_service()
    # await scheduler_service.set_all_jobs()
    logs_config.config()
    app.include_router(router)
    yield
app = FastAPI(lifespan=lifespan)


async def init_models():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == '__main__':
    asyncio.run(init_models())
    pass
