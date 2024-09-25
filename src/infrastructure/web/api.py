from fastapi import Depends, APIRouter, Path, Response, status, BackgroundTasks
from sqlalchemy.orm import Session

from application.services.lego_sets_service import LegoSetsService
# from application.services.scheduler_service import SchedulerService
from infrastructure.config.logs_config import log_api_decorator
from infrastructure.config.services_config import get_lego_sets_service

router = APIRouter()

async def get_result_json(data: dict):
    return {
        'meta':
            {
                'code': "200",
                'message': "OK",
                'description': "OK"
            },
        'result': data
    }

@router.get("/")
@log_api_decorator
async def empty(response: Response, background_tasks: BackgroundTasks):
    return await get_result_json(data={'message': "API is working"})


@router.post("/sets/parse")
@log_api_decorator
async def parse_sets(response: Response, background_tasks: BackgroundTasks,
                  lego_sets_service: LegoSetsService = Depends(get_lego_sets_service)):
    background_tasks.add_task(lego_sets_service.async_parse_all_sets)
    # data = await lego_sets_service.parse_all_sets()
    return await get_result_json(data={'status': 'parse start'})


@router.get("/sets/{set_id}")
@log_api_decorator
async def get_set(set_id: str, response: Response, background_tasks: BackgroundTasks,
                  lego_sets_service: LegoSetsService = Depends(get_lego_sets_service)):
    data = await lego_sets_service.get_set_info(set_id=set_id)
    return await get_result_json(data={'set_info': data})

