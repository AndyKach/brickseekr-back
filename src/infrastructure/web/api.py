from typing import Any, Dict

from fastapi import Depends, APIRouter, Path, Response, status, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from application.services.legosets_service import LegoSetsService
from domain.legoset import LegoSet
from domain.legosets_price import LegoSetsPrice
from domain.legosets_prices import LegoSetsPrices
# from application.services.scheduler_service import SchedulerService
from infrastructure.config.logs_config import log_api_decorator
from infrastructure.config.services_config import get_lego_sets_service
from infrastructure.config.fastapi_app_config import app
from infrastructure.web.setup import setup

setup()

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
@log_api_decorator
async def empty(response: Response, background_tasks: BackgroundTasks):
    return await get_success_json_response(data={'message': "API is working"})


# @app.get('/sets/parseAllSetsAllStores')
@app.get("/sets/{set_id}/getData", tags=['Sets'], response_model=LegoSet)
@log_api_decorator
async def get_set(set_id: str, response: Response, background_tasks: BackgroundTasks,
                  lego_sets_service: LegoSetsService = Depends(get_lego_sets_service)):
    data = await lego_sets_service.get_legoset_info(legoset_id=set_id)
    # print(f"data: {data}")
    if data is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
    else:
        return await get_success_json_response(data=data)

@app.get("/sets/{set_id}/getPrices", tags=['Sets'], response_model=LegoSetsPrices)
@log_api_decorator
async def get_sets_prices(
        set_id: str, response: Response, background_tasks: BackgroundTasks,
        lego_sets_service: LegoSetsService = Depends(get_lego_sets_service)
    ):
    data = await lego_sets_service.get_sets_prices(set_id=set_id)
    if data is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
    else:
        return await get_success_json_response(data=data)

@app.get('/sets/{set_id}/stores/{store_id}/getPrice', tags=['Sets'], response_model=LegoSetsPrice)
@log_api_decorator
async def get_sets_prices_from_website(
        set_id: str, website_id: int, response: Response, background_tasks: BackgroundTasks,
        lego_sets_service: LegoSetsService = Depends(get_lego_sets_service)
    ):
    data = await lego_sets_service.get_sets_prices_from_website(set_id=set_id, website_id=website_id)
    if data is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
    else:
        return await get_success_json_response(data=data)

# @app.get('/sets/{set_id}/parseAllStores')

# @app.get('/sets/{set_id}/{store_id}/parseSet')

# @app.get('/store/{store_id}/parseAllSets')
# ''









# @app.post("/sets/parseKnownSets", tags=['Experimental'])
# @log_api_decorator
# async def parse_sets(
#         response: Response, background_tasks: BackgroundTasks,
#         response_model=ResponseModel,
#         lego_sets_service: LegoSetsService = Depends(get_lego_sets_service),
# ):
#     background_tasks.add_task(lego_sets_service.async_parse_all_known_sets)
#     # data = await lego_sets_service.parse_all_sets()
#     return await get_success_json_response(data={'status': 'parse start'})
#
#
# @app.post("/sets/parseUnknownSets", tags=['Experimental'])
# @log_api_decorator
# async def parse_sets(
#         response: Response, background_tasks: BackgroundTasks,
#         lego_sets_service: LegoSetsService = Depends(get_lego_sets_service),
# ):
#     background_tasks.add_task(lego_sets_service.async_parse_all_unknown_sets)
#     # data = await lego_sets_service.parse_all_sets()
#     return await get_success_json_response(data={'status': 'parse start'})

@app.post("/parseSetsFromBrickSet", tags=['Experimental'])
@log_api_decorator
async def parse_sets_from_brickset(
        response: Response, background_tasks: BackgroundTasks,
        lego_sets_service: LegoSetsService = Depends(get_lego_sets_service),
):
    background_tasks.add_task(lego_sets_service.parse_sets_from_brickset)
    # data = await lego_sets_service.parse_all_sets()
    return await get_success_json_response(data={'status': 'parse start'})


@app.post("parseLegoSetFromLego", tags=['Experimental'])
@log_api_decorator
async def parse_sets_from_lego(
        legoset_id: str,
        response: Response, background_tasks: BackgroundTasks,
        lego_sets_service: LegoSetsService = Depends(get_lego_sets_service),
):
    background_tasks.add_task()
    # data = await lego_sets_service.parse_all_sets()
    return await get_success_json_response(data={'status': 'parse start'})











# @app.post("/sets/{set_id}/parse")
# @log_api_decorator
# async def parse_sets(
#         set_id: str,
#         response: Response, background_tasks: BackgroundTasks,
#         lego_sets_service: LegoSetsService = Depends(get_lego_sets_service),
# ):
#     background_tasks.add_task(lego_sets_service.async_parse_set, set_id)
#
#     # data = await lego_sets_service.parse_all_sets()
#     return await get_success_json_response(data={'status': 'parse start'})
#
# @app.get("/{store}/sets/parseSets")
# @log_api_decorator
# async def parse_sets(
#         store: str,
#         response: Response, background_tasks: BackgroundTasks,
#         lego_sets_service: LegoSetsService = Depends(get_lego_sets_service),
# ):
#     background_tasks.add_task(lego_sets_service.async_parse_sets, store=store)
#     # data = await lego_sets_service.parse_all_sets()
#     return await get_success_json_response(data={'status': 'parse start'})

@app.post("/sets/{set_id}/stores/{store_id}/parseSet", tags=['Experimental'])
async def parse_set_in_store(
        set_id: str, store_id: str,
        response: Response, background_tasks: BackgroundTasks,
        lego_sets_service: LegoSetsService = Depends(get_lego_sets_service),
):
    result = await lego_sets_service.parse_set_in_store(set_id=set_id, store_id=store_id)
    return await get_success_json_response(data={'lego_set_id': set_id, 'price': result})



@app.get("/sets/parseSetsUrls", tags=['Experimental'])
@log_api_decorator
async def parse_sets(
        response: Response, background_tasks: BackgroundTasks,
        lego_sets_service: LegoSetsService = Depends(get_lego_sets_service),
):
    background_tasks.add_task(lego_sets_service.parse_lego_sets_urls)
    # data = await lego_sets_service.parse_all_sets()
    return await get_success_json_response(data={'status': 'parse start'})


@app.post("/stores/{store_id}/parseAllSets", tags=['Experimental'])
@log_api_decorator
async def parse_sets(
        store_id: str,
        response: Response, background_tasks: BackgroundTasks,
        lego_sets_service: LegoSetsService = Depends(get_lego_sets_service),
):
    background_tasks.add_task(lego_sets_service.parse_all_sets_in_store, store_id=store_id)
    # data = await lego_sets_service.parse_all_sets()
    return await get_success_json_response(data={'status': 'parse start'})


