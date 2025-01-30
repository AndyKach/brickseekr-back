from application.interfaces.website_interface import WebsiteInterface
from application.repositories.legosets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository

import logging

from application.use_cases.lego_sets_prices_save_use_case import LegoSetsPricesSaveUseCase
from application.use_cases.website_parser_use_case import WebsiteParserUseCase

system_logger = logging.getLogger('system_logger')


class WebsiteSparkysParserUseCase(WebsiteParserUseCase):
    def __init__(self,
                 lego_sets_repository: LegoSetsRepository,
                 lego_sets_prices_repository: LegoSetsPricesRepository,
                 website_interface: WebsiteInterface,
                 ):
        self.lego_sets_repository = lego_sets_repository
        self.lego_sets_prices_repository = lego_sets_prices_repository
        self.website_interface = website_interface


        self.lego_sets_prices_save_use_case = LegoSetsPricesSaveUseCase(
            lego_sets_prices_repository=self.lego_sets_prices_repository
        )

        self.website_id = 3

    async def parse_legosets_price(self, legoset_id: str):
        lego_set = await self.lego_sets_repository.get_set(set_id=legoset_id)
        await self._parse_item(
            legoset=lego_set,
            website_interface=self.website_interface,
            legosets_prices_save_use_case=self.lego_sets_prices_save_use_case,
            website_id=self.website_id
        )

    async def parse_legosets_prices(self):
        lego_sets = await self.lego_sets_repository.get_all()
        await self._parse_items(
            legosets=lego_sets,
            website_interface=self.website_interface,
            legosets_prices_save_use_case=self.lego_sets_prices_save_use_case,
            website_id=self.website_id
        )
