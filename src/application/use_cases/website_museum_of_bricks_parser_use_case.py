import logging

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
    async def parse_legosets_url(self, legoset_id: str):
        legoset_url = await self.website_interface.parse_legosets_url(legoset_id=legoset_id)
        if legoset_url:
            await self.legosets_repository.update_url_name(lego_set_id=legoset_id, url_name=legoset_url)

    @log_decorator()
    async def parse_legosets_urls(self):
        legosets = await self.legosets_repository.get_all()
        for i in range(120, 5745, 100):
            result = await self.website_interface.parse_legosets_urls(lego_sets=legosets[i:i+100])
        # print('!!!!!!!\n{result}\n!!!!!!!'.format(result=result))
            for lego_set in result:
                await self.legosets_repository.update_url_name(
                    lego_set_id=lego_set["id"], url_name=lego_set['url']
                )

    @log_decorator()
    async def parse_legosets_price(self, legoset_id: str):
        legoset = await self.legosets_repository.get_set(set_id=legoset_id)
        if legoset.extendedData.get('cz_url_name') == "None":
            await self.parse_legosets_url(legoset_id=legoset_id)
        await self._parse_item(
            legoset=legoset,
            website_interface=self.website_interface,
            legosets_repository=self.legosets_repository,
            legosets_prices_save_use_case=self.lego_sets_prices_save_use_case,
            website_id=self.website_id
        )

    @log_decorator()
    async def parse_legosets_prices(self):
        legosets = await self.legosets_repository.get_all()
        for legoset in legosets:
            if legoset.extendedData.get('cz_url_name') == "None":
                await self.parse_legosets_url(legoset_id=legoset.id)
        await self._parse_items(
            legosets=legosets[4255:4700],
            website_interface=self.website_interface,
            legosets_repository=self.legosets_repository,
            legosets_prices_save_use_case=self.lego_sets_prices_save_use_case,
            website_id=self.website_id
        )

    # async def parse_lego_sets_price(self, lego_set_id: str):
    #     lego_set = await self.lego_sets_repository.get_set(set_id=lego_set_id)
    #     result = await self.website_interface.parse_lego_sets_price(lego_set=lego_set)
    #     system_logger.info(f"Lego set {lego_set.lego_set_id} - {result}")
    #     await self.lego_sets_prices_save_use_case.save_lego_sets_price(
    #         LegoSetsPrice(
    #             lego_set_id=lego_set.lego_set_id,
    #             price=result.get('price'),
    #             website_id=self.website_id
    #         )
    #     )
    #     return result
    #
    # async def parse_lego_sets_prices(self):
    #     lego_sets = await self.lego_sets_repository.get_all()
    #     for i in range(1, len(lego_sets), 100):
    #         results = await self.website_interface.parse_lego_sets_prices(lego_sets=lego_sets[i:i+100])
    #         system_logger.info(f"Result: {results}")
    #
    #         for result in results:
    #             if result is not None:
    #                 await self.lego_sets_prices_save_use_case.save_lego_sets_price(
    #                     LegoSetsPrice(
    #                         lego_set_id=result.get('lego_set_id'),
    #                         price=result.get('price'),
    #                         website_id=self.website_id
    #                     )
    #                 )




