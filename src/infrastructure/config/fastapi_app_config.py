import uvicorn
import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from icecream import ic

from infrastructure.config import logs_config

from infrastructure.config.services_config import get_scheduler_service


system_logger = logging.getLogger("system_logger")
error_logger = logging.getLogger("error_logger")

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler_service = get_scheduler_service()
    await scheduler_service.set_all_jobs()
    # ic(await scheduler_service.get_all_jobs())
    logs_config.config()
    # app.include_router(router)
    yield
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def config():
    system_logger.info("Start uvicorn configuration")
    uvicorn.run(app, host=os.getenv("WEBAPP_HOST", "127.0.0.1"), port=int(os.getenv("WEBAPP_PORT", 8000)))
