from typing import Any, Dict

from fastapi import Depends, APIRouter, Path, Response, status, BackgroundTasks, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from application.services.lego_sets_service import LegoSetsService
# from application.services.scheduler_service import SchedulerService
from infrastructure.config.logs_config import log_api_decorator
from infrastructure.config.services_config import get_lego_sets_service
from infrastructure.config.fastapi_app_config import app

# router = APIRouter()

class Meta(BaseModel):
    code: str
    message: str
    description: str

class ResponseModel(BaseModel):
    meta: Meta
    result: Any

async def get_success_json_response(data: dict):
    response = ResponseModel(
        meta=Meta(
            code="200",
            message="OK",
            description="Item fetched successfully"
        ),
        result=data
    )
    return response


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc: HTTPException):
    # Формирование стандартного ответа при ошибке
    response = ResponseModel(
        meta=Meta(
            code=str(exc.status_code),
            message="Error",
            description=exc.detail
        ),
        result={}
    )
    return response

@app.get("/")
@log_api_decorator
async def empty(response: Response, background_tasks: BackgroundTasks):
    return await get_success_json_response(data={'message': "API is working"})


@app.post("/sets/parseKnownSets")
@log_api_decorator
async def parse_sets(
        response: Response, background_tasks: BackgroundTasks,
        response_model=ResponseModel,
        lego_sets_service: LegoSetsService = Depends(get_lego_sets_service),
):
    background_tasks.add_task(lego_sets_service.async_parse_all_known_sets)
    # data = await lego_sets_service.parse_all_sets()
    return await get_success_json_response(data={'status': 'parse start'})


@app.post("/sets/parseUnknownSets")
@log_api_decorator
async def parse_sets(
        response: Response, background_tasks: BackgroundTasks,
        response_model: BaseModel = ResponseModel,
        lego_sets_service: LegoSetsService = Depends(get_lego_sets_service),
):
    background_tasks.add_task(lego_sets_service.async_parse_all_unknown_sets)
    # data = await lego_sets_service.parse_all_sets()
    return await get_success_json_response(data={'status': 'parse start'})



@app.get("/sets/{set_id}")
@log_api_decorator
async def get_set(set_id: str, response: Response, background_tasks: BackgroundTasks,
                  lego_sets_service: LegoSetsService = Depends(get_lego_sets_service)):
    data = await lego_sets_service.get_set_info(set_id=set_id)
    print(data)
    if data is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
    else:
        return await get_success_json_response(data=data)


@app.get("/sets/{set_id}/prices")
@log_api_decorator
async def get_sets_prices(
        set_id: str, response: Response, background_tasks: BackgroundTasks,
        lego_sets_service: LegoSetsService = Depends(get_lego_sets_service)
    ):
    data = await lego_sets_service.get_sets_prices(set_id=set_id)
    return await get_success_json_response(data=data)



@app.get("/sets/{set_id}/prices/{website_id}")
@log_api_decorator
async def get_sets_prices_from_website(
        set_id: str, website_id: str, response: Response, background_tasks: BackgroundTasks,
        lego_sets_service: LegoSetsService = Depends(get_lego_sets_service)
    ):
    data = await lego_sets_service.get_sets_prices_from_website(set_id=set_id, website_id=website_id)
    return await get_success_json_response(data=data)

@app.post("/sets/{set_id}/parse")
@log_api_decorator
async def parse_sets(
        set_id: str,
        response: Response, background_tasks: BackgroundTasks,
        lego_sets_service: LegoSetsService = Depends(get_lego_sets_service),
):
    background_tasks.add_task(lego_sets_service.async_parse_set, set_id)

    # data = await lego_sets_service.parse_all_sets()
    return await get_success_json_response(data={'status': 'parse start'})



