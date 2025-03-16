import logging

from icecream import ic

from application.interfaces.website_interface import WebsiteInterface
from application.repositories.legosets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
import aiohttp
import asyncio
from aiolimiter import AsyncLimiter
from aiohttp.client_exceptions import TooManyRedirects

from application.use_cases.lego_sets_prices_save_use_case import LegoSetsPricesSaveUseCase
from application.use_cases.website_parser_use_case import WebsiteParserUseCase
from domain.legosets_price import LegoSetsPrice
from domain.legosets_prices import LegoSetsPrices
from infrastructure.config.logs_config import log_decorator

system_logger = logging.getLogger('system_logger')

class WebsiteMuseumOfBricksParserUseCase(WebsiteParserUseCase):
    def __init__(self,
                 lego_sets_repository: LegoSetsRepository,
                 lego_sets_prices_repository: LegoSetsPricesRepository,
                 website_interface: WebsiteInterface,
                 ):
        self.legosets_repository = lego_sets_repository
        self.legosets_prices_repository = lego_sets_prices_repository
        self.website_interface = website_interface
        self.lego_sets_prices_save_use_case = LegoSetsPricesSaveUseCase(
            legosets_prices_repository=self.legosets_prices_repository
        )

        self.website_id = "4"

    @log_decorator()
    async def parse_legosets_price(self, legoset_id: str):
        legoset = await self.legosets_repository.get_set(set_id=legoset_id)
        await self._parse_item(
            legoset=legoset,
            website_interface=self.website_interface,
            legosets_prices_save_use_case=self.lego_sets_prices_save_use_case,
            website_id=self.website_id
        )

    @log_decorator()
    async def parse_legosets_prices(self):
        legosets = [legoset for legoset in await self.legosets_repository.get_all() if legoset.year > 2020]
        system_logger.info(f"Count of legosets for parse: {len(legosets)}")
        await self._parse_items(
            legosets=legosets,
            website_interface=self.website_interface,
            legosets_prices_save_use_case=self.lego_sets_prices_save_use_case,
            website_id=self.website_id
        )

    @log_decorator()
    async def parse_legosets_url(self, legoset_id: str):
        # TODO переделать под более нормальную версию
        legoset_url = await self.website_interface.parse_legosets_url(legoset_id=legoset_id)
        if legoset_url:
            await self.legosets_repository.update_url_name(lego_set_id=legoset_id, url_name=legoset_url)

    @log_decorator()
    async def parse_legosets_urls(self):
        # TODO переделать под более нормальную версию
        # legosets = [legoset for legoset in await self.legosets_repository.get_all() if (legoset.rating != 0 and legoset.year > 2018)]
        legosets = [legoset for legoset in await self.legosets_repository.get_all() if (legoset.rating != 0 and legoset.extendedData.get('cz_url_name') != "None")]
        print(len(legosets))
        step = 150
        # legosets = legosets.reverse()

        # for i in range(len(legosets), 0, -step):
        for i in range(0, 1, step):
            break
            results = await self.website_interface.parse_legosets_urls(legosets=legosets[i-step:i])
            ic(results)
            for result in results:
                if result.get('status') == 200:
                    system_logger.info(f"Legoset {result.get('id')} has cz_url: {result.get('url')} cz_category: {result.get('category')}")
                    try:
                        await self.legosets_repository.update_extended_data(
                            legoset_id=result.get('id'),
                            extended_data={
                                'cz_url_name': result.get('url'),
                                'cz_category_name': result.get('category')
                            },
                        )
                    except Exception as e:
                        system_logger.error(e)

                elif result.get('status') == 404:
                    system_logger.info(f"Legoset {result.get('id')} was not found")
        # print('!!!!!!!\n{result}\n!!!!!!!'.format(result=result))
        #     for lego_set in result:
                # await self.legosets_repository.update_url_name(
                #     lego_set_id=lego_set["id"], url_name=lego_set['url']
                # )




