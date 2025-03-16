import logging
from typing import Any, Dict
import re
from fastapi import Depends, APIRouter, Path, Response, status, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from application.services.legosets_service import LegoSetsService
from domain.legoset import Legoset
from domain.legosets_price import LegoSetsPrice
from domain.legosets_prices import LegoSetsPrices
# from application.services.scheduler_service import SchedulerService
from infrastructure.config.logs_config import log_api_decorator
from infrastructure.config.services_config import get_legosets_service
from infrastructure.config.fastapi_app_config import app
from infrastructure.web.response_models import GetDataResponseModel, GetLegosetsTopRatingResponseModel
# from infrastructure.web.setup import setup
#
# setup()
system_logger = logging.getLogger("system_logger")
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
    return JSONResponse(content=response.model_dump(), status_code=200)


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
    return JSONResponse(content=response.model_dump(), status_code=exc.status_code)

@app.get("/")
@log_api_decorator()
async def empty(response: Response, background_tasks: BackgroundTasks):
    return await get_success_json_response(data={'message': "API is working"})


# @app.get('/sets/parseAllSetsAllStores')
@log_api_decorator()
@app.get("/sets/{set_id}/getData", tags=['Sets'], response_model=GetDataResponseModel,
         responses={'422': {"model": ResponseModel, 'description': "Validation Error"},
                    '404': {"model": ResponseModel, 'description': "Not Found"},
                    '500': {"model": ResponseModel, 'description': "Internal Server Error"},})
async def get_set(set_id: str, response: Response, background_tasks: BackgroundTasks,
                  legosets_service: LegoSetsService = Depends(get_legosets_service)):
    if await validate_legoset_id(legoset_id=set_id):
        data = None
        try:
            data = await legosets_service.get_legoset_info(legoset_id=set_id)
        except Exception as e:
            system_logger.error(f"Error by API /getData: {e}")
            await raise_internal_server_error()

        if data is None:
            await raise_item_not_found()
        else:
            return await get_success_json_response(data=data)
    else:
        await raise_validation_error(detail="Legoset ID is not valid")

@log_api_decorator()
@app.get('/sets/{set_id}/getLegosetsTopRating', tags=['Sets'], response_model=GetLegosetsTopRatingResponseModel,
         responses={'422': {"model": ResponseModel, 'description': "Validation Error"},
                    '404': {"model": ResponseModel, 'description': "Not Found"},
                    '500': {"model": ResponseModel, 'description': "Internal Server Error"},})
async def get_rating_top_list(
        legosets_count: int, response: Response, background_tasks: BackgroundTasks,
        legosets_service: LegoSetsService = Depends(get_legosets_service)
    ):
    if legosets_count > 0:
        data = None
        try:
            data = await legosets_service.get_legosets_rating_list(legosets_count=legosets_count)
        except Exception as e:
            system_logger.error(f"Error by API /getLegosetsTopRating: {e}")
            await raise_internal_server_error()

        if data is None:
            await raise_item_not_found()
        else:
            return await get_success_json_response(data=data)
    else:
        raise HTTPException(500)

@log_api_decorator()
@app.post('/sets/calculateRating', tags=['Sets'])
async def calculate_rating(
        response: Response, background_tasks: BackgroundTasks,
        legosets_service: LegoSetsService = Depends(get_legosets_service)
):
    data = None
    try:
        data = await legosets_service.recalculate_rating()
    except Exception as e:
        system_logger.error(f"Error by API /calculateRating: {e}")
        await raise_internal_server_error()

    if data is None:
        await raise_item_not_found()
    else:
        return await get_success_json_response(data={"result": data})


@log_api_decorator()
@app.get("/sets/{set_id}/getPrices", tags=['Sets'], response_model=LegoSetsPrices)
async def get_sets_prices(
        set_id: str, response: Response, background_tasks: BackgroundTasks,
        legosets_service: LegoSetsService = Depends(get_legosets_service)
    ):
    data = await legosets_service.get_sets_prices(set_id=set_id)
    if data is None:
        await raise_item_not_found()
    else:
        return await get_success_json_response(data=data)

@log_api_decorator()
@app.get('/sets/{set_id}/stores/{store_id}/getPrice', tags=['Sets'], response_model=LegoSetsPrice)
async def get_sets_prices_from_website(
        set_id: str, website_id: str, response: Response, background_tasks: BackgroundTasks,
        legosets_service: LegoSetsService = Depends(get_legosets_service)
    ):
    data = await legosets_service.get_sets_prices_from_website(set_id=set_id, website_id=website_id)
    if data is None:
        await raise_item_not_found()
    else:
        return await get_success_json_response(data=data)

@log_api_decorator()
@app.post('/sets/{set_id}/parseImages', tags=['Experimental'])
async def parse_legoset_images(
        set_id: str,
        response: Response, background_tasks: BackgroundTasks,
        legosets_service: LegoSetsService = Depends(get_legosets_service)
    ):
    data = await legosets_service.parse_legoset_images(legoset_id=set_id)
    if data is None:
        await raise_item_not_found()
    else:
        return await get_success_json_response(data={"result": data})

@log_api_decorator()
@app.post('/sets/parseImages', tags=['Experimental'])
async def parse_legosets_images(
        response: Response, background_tasks: BackgroundTasks,
        legosets_service: LegoSetsService = Depends(get_legosets_service)
    ):
    data = await legosets_service.parse_legosets_images()
    if data is None:
        await raise_item_not_found()
    else:
        return await get_success_json_response(data={"result": data})


@log_api_decorator()
@app.post("/parseSetsFromBrickSet", tags=['Experimental'])
async def parse_sets_from_brickset(
        response: Response, background_tasks: BackgroundTasks,
        legosets_service: LegoSetsService = Depends(get_legosets_service),
):
    background_tasks.add_task(legosets_service.parse_sets_from_brickset)
    return await get_success_json_response(data={'status': 'parse start'})

@log_api_decorator()
@app.post("/parseLegoSetFromLego", tags=['Experimental'])
async def parse_sets_from_lego(
        response: Response, background_tasks: BackgroundTasks,
        legosets_service: LegoSetsService = Depends(get_legosets_service),
):
    background_tasks.add_task(legosets_service.parse_legosets_from_lego)
    return await get_success_json_response(data={'status': 'parse start'})


@log_api_decorator()
@app.post("/sets/parseSetsUrl", tags=['Experimental'])
async def parse_sets_url(
        response: Response, background_tasks: BackgroundTasks,
        legosets_service: LegoSetsService = Depends(get_legosets_service),
):
    background_tasks.add_task(legosets_service.parse_lego_sets_url)
    return await get_success_json_response(data={'status': 'parse start'})

@log_api_decorator()
@app.post("/sets/parseSetsUrls", tags=['Experimental'])
async def parse_sets_urls(
        response: Response, background_tasks: BackgroundTasks,
        legosets_service: LegoSetsService = Depends(get_legosets_service),
):
    background_tasks.add_task(legosets_service.parse_lego_sets_urls)
    return await get_success_json_response(data={'status': 'parse start'})


@log_api_decorator()
@app.post("/sets/{set_id}/stores/{store_id}/parseSetsPrice", tags=['Experimental'])
async def parse_sets_price_in_store(
        set_id: str, store_id: str,
        response: Response, background_tasks: BackgroundTasks,
        legosets_service: LegoSetsService = Depends(get_legosets_service),
):
    result = await legosets_service.parse_legosets_price_in_store(set_id=set_id, store_id=store_id)
    return await get_success_json_response(data={'status': 'parse start'})


@log_api_decorator()
@app.post("/stores/{store_id}/parseAllSetsPrices", tags=['Experimental'])
async def parse_all_sets_prices_in_store(
        store_id: str,
        response: Response, background_tasks: BackgroundTasks,
        legosets_service: LegoSetsService = Depends(get_legosets_service),
):
    background_tasks.add_task(legosets_service.parse_all_legosets_in_store, store_id=store_id)
    return await get_success_json_response(data={'status': 'parse start'})


async def validate_legoset_id(legoset_id: str) -> bool:
    pattern = r'^(?!0{5})\d{5}$'
    return bool(re.fullmatch(pattern, legoset_id))


async def raise_internal_server_error() -> None:
    raise HTTPException(
        status_code=500,
        detail="Internal server error"
    )

async def raise_item_not_found() -> None:
    raise HTTPException(
        status_code=404,
        detail="Item not found"
    )

async def raise_validation_error(detail: str = "") -> None:
    raise HTTPException(
        status_code=422,
        detail="Validation error" + ("" if detail == "" else f": {detail}")
    )
