import logging
from application.interfaces.website_interface import WebsiteInterface
from application.repositories.legosets_repository import LegosetsRepository
from application.repositories.prices_repository import LegosetsPricesRepository
from application.use_cases.legosets_prices_save_use_case import LegosetsPricesSaveUseCase
from application.use_cases.website_parser_use_case import WebsiteParserUseCase

system_logger = logging.getLogger('system_logger')

class WebsiteKostickyShopParserUseCase(WebsiteParserUseCase):
    def __init__(self,
                 legosets_repository: LegosetsRepository,
                 legosets_prices_repository: LegosetsPricesRepository,
                 website_interface: WebsiteInterface,
                 ):
        self.legosets_repository = legosets_repository
        self.legosets_prices_repository = legosets_prices_repository
        self.website_interface = website_interface

        self.legosets_prices_save_use_case = LegosetsPricesSaveUseCase(
            legosets_prices_repository=self.legosets_prices_repository
        )
        self.website_id = "5"


    async def parse_legosets_price(self, legoset_id: str):
        legoset = await self.legosets_repository.get_set(set_id=legoset_id)
        await self._parse_item(
            legoset=legoset,
            website_interface=self.website_interface,
            legosets_prices_save_use_case=self.legosets_prices_save_use_case,
            website_id=self.website_id
        )

    async def parse_legosets_prices(self):
        legosets = [legoset for legoset in await self.legosets_repository.get_all() if legoset.year > 2020]
        system_logger.info(f"Count of legosets for parse: {len(legosets)}")
        await self._parse_items(
            legosets=legosets,
            website_interface=self.website_interface,
            legosets_prices_save_use_case=self.legosets_prices_save_use_case,
            website_id=self.website_id
        )
