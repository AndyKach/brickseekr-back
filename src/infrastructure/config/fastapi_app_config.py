import uvicorn
import logging
import os

from fastapi import FastAPI
from contextlib import asynccontextmanager
from infrastructure.config import logs_config

from infrastructure.config.services_config import get_scheduler_service


system_logger = logging.getLogger("system_logger")
error_logger = logging.getLogger("error_logger")

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler_service = get_scheduler_service()
    await scheduler_service.set_all_jobs()
    logs_config.config()
    # app.include_router(router)
    yield
app = FastAPI(lifespan=lifespan)

def config():
    system_logger.info("Start uvicorn configuration")
    uvicorn.run(app, host=os.getenv("WEBAPP_HOST", "127.0.0.1"), port=int(os.getenv("WEBAPP_PORT", 8000)))
