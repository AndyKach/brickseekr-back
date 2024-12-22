import asyncio
from datetime import datetime

from icecream import ic
from requests.utils import extract_zipped_paths

from application.interfaces.website_interface import WebsiteInterface
from application.repositories.lego_sets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from application.use_cases.website_parser_use_case import WebsiteParserUseCase
from domain.lego_set import LegoSet
from domain.lego_sets_prices import LegoSetsPrices
import logging

system_logger = logging.getLogger('system_logger')


class WebsiteLegoParserUseCase(WebsiteParserUseCase):
    def __init__(
            self,
            lego_sets_prices_repository: LegoSetsPricesRepository,
            lego_sets_repository: LegoSetsRepository,
            website_lego_interface: WebsiteInterface,
    ):
        self.lego_sets_repository = lego_sets_repository
        self.lego_sets_prices_repository = lego_sets_prices_repository
        self.website_lego_interface = website_lego_interface

        self.website_id = '1'

    async def parse_item(self):
        pass

    async def parse_items(self):
        lego_sets = await self.lego_sets_repository.get_all()
        await self._parse_items(
            lego_sets=lego_sets[4255:4700],
            website_interface=self.website_lego_interface,
            lego_sets_prices_repository=self.lego_sets_prices_repository,
            website_id=self.website_id
        )

    async def parse_known_sets(self):
        """
        Parse sets from lego_sets_prices
        """
        lego_sets = await self.lego_sets_prices_repository.get_all_items()
        # print(lego_sets)
        await self._parse_items(lego_sets=lego_sets)

    async def parse_all_sets(self):
        """
        Parse sets from lego_sets
        """
        lego_sets = await self.lego_sets_repository.get_all()
        await self._parse_items(lego_sets=lego_sets)

    async def parse_set(self, lego_set_id: str):
        await self._parse_item(lego_set_id=lego_set_id)

    async def _parse_item(self, lego_set_id: str):
        time_start = datetime.now()

        item_info = await self.website_lego_interface.parse_lego_sets_price(lego_set=lego_set_id)
        if item_info is not None:
            lego_sets_prices = LegoSetsPrices(
                lego_set_id=item_info.get('lego_set_id'),
                prices={self.website_id: item_info.get('price')}
            )
            await self._save_new_price(lego_sets_prices=lego_sets_prices)

        system_logger.info(f'Parse is end in {datetime.now() - time_start}')
