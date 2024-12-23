import asyncio
from datetime import datetime

from icecream import ic
from requests.utils import extract_zipped_paths
from watchfiles import awatch

from application.interfaces.website_interface import WebsiteInterface
from application.repositories.lego_sets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from application.use_cases.lego_sets_prices_save_use_case import LegoSetsPricesSaveUseCase
from application.use_cases.website_parser_use_case import WebsiteParserUseCase
from domain.lego_set import LegoSet
from domain.lego_sets_prices import LegoSetsPrices
import logging

system_logger = logging.getLogger('system_logger')

class WebsiteCapiCapParserUseCase(WebsiteParserUseCase):
    def __init__(
            self,
            lego_sets_prices_repository: LegoSetsPricesRepository,
            lego_sets_repository: LegoSetsRepository,
            website_interface: WebsiteInterface
    ):
        self.lego_sets_repository = lego_sets_repository
        self.lego_sets_prices_repository = lego_sets_prices_repository
        self.website_interface = website_interface
        self.lego_sets_prices_save_use_case = LegoSetsPricesSaveUseCase(
            lego_sets_prices_repository=self.lego_sets_prices_repository
        )

        self.website_id = "2"

    async def parse_lego_sets_price(self, lego_set_id: str):
        lego_set = await self.lego_sets_repository.get_set(set_id=lego_set_id)
        await self._parse_item(
            lego_set=lego_set,
            website_interface=self.website_interface,
            lego_sets_prices_save_use_case=self.lego_sets_prices_save_use_case,
            website_id=self.website_id
        )


    async def parse_lego_sets_prices(self):
        lego_sets = await self.lego_sets_repository.get_all()
        await self._parse_items(
            lego_sets=lego_sets,
            website_interface=self.website_interface,
            lego_sets_prices_save_use_case=self.lego_sets_prices_save_use_case,
            website_id=self.website_id
        )


