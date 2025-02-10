from datetime import datetime
import time
import os
import aiohttp
import asyncio
import json
from icecream import ic
from dotenv import load_dotenv

import logging
from application.interfaces.website_data_source_interface import WebsiteDataSourceInterface
from application.interfaces.website_interface import WebsiteInterface
from application.repositories.legosets_repository import LegoSetsRepository
from domain.strings_tool_kit import StringsToolKit
from infrastructure.config.logs_config import log_decorator
from domain.legoset import LegoSet

load_dotenv()

system_logger = logging.getLogger('system_logger')


class WebsiteBricksetInterface(WebsiteDataSourceInterface, StringsToolKit):

    def __init__(self):
        super().__init__()
        self.driver = None
        self.waiting_time = 2
        self.url = "https://brickset.com"
        self.url_api = "https://brickset.com/api/v3.asmx"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'de-DE,de;q=0.9',
        }
        self.params = {
            'apiKey': os.getenv("BRICKSET_API_TOKEN"),
            'userHash': os.getenv("BRICKSET_USER_HASH"),
        }
        self.response = None

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legosets(self, legosets_repository: LegoSetsRepository):
        last_datetime = datetime.now()
        log_text = ""
        count_saves_legosets = 0
        count_to_parse = 2
        results = []
        for year in range(2025, 2009, -count_to_parse):
            # time.sleep(2)
            system_logger.info(f"Year {year} is started")
            async with aiohttp.ClientSession() as session:

                # tasks = [self.request_get_legoset(session=session, legoset_id=k) for k in range(year, year + count_to_parse)]
                tasks1 = [self.request_get_legosets_per_year(session=session, year=k) for k in
                          range(year, year - count_to_parse, -1)]
                tasks2 = [self.request_get_legosets_per_year(session, year=k, page_number=2) for k in
                          range(year, year - count_to_parse, -1)]
                ic(tasks2)
                # Параллельное выполнение всех задач
                results1 = await asyncio.gather(*tasks1)
                results2 = await asyncio.gather(*tasks2)
            # ic(results2)
            results = results1 + results2
            for result in results:
                if result:
                    if result.get('status') == "success" and result.get('matches') != 0:
                        sets = result.get('sets')
                        # ic(sets)
                        for index, legoset_json in enumerate(sets):
                            if index % 15 == 0:
                                system_logger.info(
                                    f"============================\nWas found {count_saves_legosets}\n{log_text[:-1]}")
                                system_logger.info(datetime.now() - last_datetime)
                                last_datetime = datetime.now()
                                log_text = ""
                            try:
                                if 10000 <= int(legoset_json.get('number')) <= 99999 and legoset_json.get(
                                        'name') != "{?}":
                                    legoset = await self.legoset_json_to_legoset(legoset_json=legoset_json)
                                    # ic(legoset)
                                    log_text += f"Legoset {legoset.id} was found in year {legoset.year} "

                                    if legoset.launchDate is not None:
                                        legoset.launchDate = datetime.strptime(legoset.launchDate, '%Y-%m-%dT%H:%M:%SZ')
                                    if legoset.exitDate is not None:
                                        legoset.exitDate = datetime.strptime(legoset.exitDate, '%Y-%m-%dT%H:%M:%SZ')
                                    if legoset.updated_at is not None:
                                        legoset.updated_at = datetime.strptime(legoset.updated_at, '%Y-%m-%dT%H:%M:%SZ')

                                    if await legosets_repository.get_set(set_id=legoset.id) is None:
                                        await legosets_repository.set_set(legoset=legoset)
                                        log_text += "and save as new\n"
                                    else:
                                        await legosets_repository.update_set(legoset=legoset)
                                        log_text += "and uploaded\n"

                                    count_saves_legosets += 1
                            except ValueError:
                                system_logger.error(f'error in set {legoset_json.get('number')}')
                                break


                    elif result.get('status') == "error":
                        system_logger.error(f"Response Error: {result}")
                else:
                    system_logger.error(f"Result Error: {result}")

            system_logger.info(f"Year {year} is ended")
            # break

    @log_decorator(print_args=False, print_kwargs=True)
    async def parse_legoset(self, legoset_id: str):
        start_datetime = datetime.now()
        async with aiohttp.ClientSession() as session:
            result = await self.request_get_legoset(session=session, legoset_id=legoset_id)
            if result:
                if result.get('status') == "success" and result.get('matches') != 0:
                    legoset_json = result.get('sets')
                    legoset = await self.legoset_json_to_legoset(legoset_json=legoset_json)

    @log_decorator(print_args=False, print_kwargs=False)
    async def request_get_legoset(self, session: aiohttp.ClientSession, legoset_id):
        url = f"{self.url_api}/getSets"
        params = self.params.copy()
        params['params'] = json.dumps({'setNumber': f"{legoset_id}-1"})
        # params = {
        #     'params': json.dumps({'setNumber': f"{legoset_id}-1"})
        # }
        async with session.get(url=url, headers=self.headers, params=params) as response:
            response_text = await response.text()
            response_json = json.loads(response_text)
            return response_json

    @log_decorator(print_args=False, print_kwargs=False)
    async def request_get_legosets_per_year(
            self,
            session: aiohttp.ClientSession,
            year: int,
            page_size: int = 500, page_number: int = 1
    ):
        url = f"{self.url_api}/getSets"
        params = self.params.copy()
        params['params'] = json.dumps({'year': year, "pageSize": page_size, "pageNumber": page_number})
        # params = {
        #     'apiKey': os.getenv("BRICKSET_API_TOKEN"),
        #     'userHash': os.getenv("BRICKSET_USER_HASH"),
        #     'params': json.dumps({'year': year, "pageSize": page_size, "pageNumber": page_number})
        # }
        async with session.get(url=url, headers=self.headers, params=params) as response:
            response_text = await response.text()
            response_json = json.loads(response_text)
            return response_json

    @staticmethod
    async def legoset_json_to_legoset(legoset_json: dict):
        return LegoSet(
            id=legoset_json.get('number'),
            images={"normalSize": legoset_json.get('image', {}).get('imageURL'),
                    "smallSize": legoset_json.get('image', {}).get('thumbnailURL')},
            name=legoset_json.get('name'),
            year=legoset_json.get('year'),
            rating=legoset_json.get('rating'),
            theme=legoset_json.get('theme'),
            themeGroup=legoset_json.get('themeGroup'),
            subtheme=legoset_json.get('subtheme'),
            pieces=legoset_json.get('pieces'),
            dimensions=legoset_json.get('dimensions'),
            weigh=0.0,
            tags=legoset_json.get('extendedData').get('tags'),
            description=legoset_json.get('extendedData').get('description'),
            ages_range=legoset_json.get('ageRange'),
            minifigures_ids=[],
            minifigures_count=legoset_json.get('minifigs'),
            extendedData={'cz_url_name': "None", 'cz_category_name': "None"},
            launchDate=legoset_json.get('launchDate'),
            exitDate=legoset_json.get('exitDate'),
            updated_at=legoset_json.get('updated_at'),
        )

    async def parse_legosets_price(self, lego_set: LegoSet) -> dict:
        pass

    async def parse_legosets_prices(self, lego_sets: list[LegoSet]):
        pass
