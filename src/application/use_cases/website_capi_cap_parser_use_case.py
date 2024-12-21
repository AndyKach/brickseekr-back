import asyncio
from datetime import datetime

from icecream import ic
from requests.utils import extract_zipped_paths
from watchfiles import awatch

from application.interfaces.website_interface import WebsiteInterface
from application.repositories.lego_sets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from application.use_cases.website_parser_use_case import WebsiteParserUseCase
from domain.lego_set import LegoSet
from domain.lego_sets_prices import LegoSetsPrices


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

    async def parse_item(self):
        pass

    async def parse_items(self):
        items = await self.lego_sets_repository.get_all()
        # print(await self.lego_sets_prices_repository.get_all_items()[:10])
        print(items[:10])
