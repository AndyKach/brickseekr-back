import asyncio
from datetime import datetime

from icecream import ic
from requests.utils import extract_zipped_paths

from application.interfaces.website_interface import WebsiteInterface
from application.repositories.lego_sets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from domain.lego_set import LegoSet
from domain.lego_sets_prices import LegoSetsPrices
from infrastructure.config.logs_config import log_decorator, system_logger


class WebsiteLegoParserUseCase:
    def __init__(
            self,
            lego_sets_prices_repository: LegoSetsPricesRepository,
            lego_sets_repository: LegoSetsRepository,
            website_interface: WebsiteInterface
    ):
        self.lego_sets_repository = lego_sets_repository
        self.lego_sets_prices_repository = lego_sets_prices_repository
        self.website_interface = website_interface

    async def parse_items(self):
        items = await self.lego_sets_repository.get_all()

