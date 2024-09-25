from fastapi import FastAPI
from contextlib import asynccontextmanager
from infrastructure.config import logs_config


@asynccontextmanager
async def lifespan(app: FastAPI):
    # scheduler_service = get_scheduler_service()
    # await scheduler_service.set_all_jobs()
    logs_config.config()
    # app.include_router(router)
    yield
app = FastAPI(lifespan=lifespan)