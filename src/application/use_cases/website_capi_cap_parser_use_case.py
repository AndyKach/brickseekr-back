import asyncio
from datetime import datetime

from icecream import ic
from requests.utils import extract_zipped_paths
from watchfiles import awatch

from application.interfaces.website_interface import WebsiteInterface
from application.repositories.legosets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from application.use_cases.lego_sets_prices_save_use_case import LegoSetsPricesSaveUseCase
from application.use_cases.website_parser_use_case import WebsiteParserUseCase
from domain.legoset import LegoSet
from domain.legosets_prices import LegoSetsPrices
import logging

system_logger = logging.getLogger('system_logger')

class WebsiteCapiCapParserUseCase(WebsiteParserUseCase):
    def __init__(
            self,
            legosets_prices_repository: LegoSetsPricesRepository,
            legosets_repository: LegoSetsRepository,
            website_interface: WebsiteInterface
    ):
        self.legosets_repository = legosets_repository
        self.legosets_prices_repository = legosets_prices_repository
        self.website_interface = website_interface
        self.legosets_prices_save_use_case = LegoSetsPricesSaveUseCase(
            legosets_prices_repository=self.legosets_prices_repository
        )

        self.website_id = "2"

    async def parse_legosets_price(self, legoset_id: str):
        legoset = await self.legosets_repository.get_set(set_id=legoset_id)
        await self._parse_item(
            legoset=legoset,
            website_interface=self.website_interface,
            legosets_repository=self.legosets_repository,
            legosets_prices_save_use_case=self.legosets_prices_save_use_case,
            website_id=self.website_id
        )


    async def parse_legosets_prices(self):
        legosets = [legoset for legoset in await self.legosets_repository.get_all() if legoset.year > 2020]
        print(len(legosets))
        # return None
        await self._parse_items(
            legosets=legosets,
            website_interface=self.website_interface,
            legosets_repository=self.legosets_repository,
            legosets_prices_save_use_case=self.legosets_prices_save_use_case,
            website_id=self.website_id
        )


