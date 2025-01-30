import asyncio
from datetime import datetime

from icecream import ic
from requests.utils import extract_zipped_paths

from application.interfaces.website_data_source_interface import WebsiteDataSourceInterface
from application.interfaces.website_interface import WebsiteInterface
from application.repositories.legosets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from application.use_cases.lego_sets_prices_save_use_case import LegoSetsPricesSaveUseCase
from application.use_cases.website_parser_use_case import WebsiteParserUseCase
from domain.legoset import LegoSet
from domain.legosets_price import LegoSetsPrice
from domain.legosets_prices import LegoSetsPrices
import logging

system_logger = logging.getLogger('system_logger')


class WebsiteLegoParserUseCase(WebsiteParserUseCase):
    def __init__(
            self,
            legosets_prices_repository: LegoSetsPricesRepository,
            legosets_repository: LegoSetsRepository,
            website_interface: WebsiteDataSourceInterface,
    ):
        self.legosets_repository = legosets_repository
        self.legosets_prices_repository = legosets_prices_repository
        self.website_interface = website_interface
        self.legosets_prices_save_use_case = LegoSetsPricesSaveUseCase(
            lego_sets_prices_repository=self.legosets_prices_repository
        )

        self.website_id = 1

    async def parse_legosets_price(self, legoset_id: str):
        legoset = await self.legosets_repository.get_set(set_id=legoset_id)
        await self._parse_item(
            legoset=legoset,
            website_interface=self.website_interface,
            legosets_prices_save_use_case=self.legosets_prices_save_use_case,
            website_id=self.website_id
        )

    async def parse_legosets_prices(self):
        lego_sets = await self.legosets_repository.get_all()
        await self._parse_items(
            legosets=lego_sets[200:220],
            website_interface=self.website_interface,
            legosets_prices_save_use_case=self.legosets_prices_save_use_case,
            website_id=self.website_id
        )

    async def parse_legosets(self):
        await self.website_interface.parse_legosets(legosets_repository=self.legosets_repository)

    # async def parse_known_sets(self):
    #     """
    #     Parse sets from lego_sets_prices
    #     """
    #     lego_sets = await self.legosets_prices_repository.get_all_items()
    #     # print(lego_sets)
    #     await self._parse_items(legosets=lego_sets)

    # async def parse_all_sets(self):
    #     """
    #     Parse sets from legosets
    #     """
    #     lego_sets = await self.legosets_repository.get_all()
    #     await self._parse_items(legosets=lego_sets)
    #
    # async def parse_set(self, lego_set_id: str):
    #     await self._parse_item(lego_set_id=lego_set_id)

    # async def _parse_item(self, lego_set_id: str):
    #     time_start = datetime.now()
    #
    #     item_info = await self.website_interface.parse_lego_sets_price(lego_set=lego_set_id)
    #     if item_info is not None:
    #         lego_sets_prices = LegoSetsPrices(
    #             lego_set_id=item_info.get('lego_set_id'),
    #             prices={self.website_id: item_info.get('price')}
    #         )
    #         await self._save_new_price(lego_sets_prices=lego_sets_prices)
    #
    #     system_logger.info(f'Parse is end in {datetime.now() - time_start}')

    # async def parse_lego_sets_price(self, lego_set_id: str):
    #     time_start = datetime.now()
    #
    #     lego_set = await self.legosets_repository.get_set(set_id=lego_set_id)
    #     result = await self.website_interface.parse_legosets_price(lego_set=lego_set)
    #     system_logger.info(f"Lego set {lego_set.lego_set_id} - {result}")
    #     await self.legosets_prices_save_use_case.save_lego_sets_price(
    #         LegoSetsPrice(
    #             legoset_id=lego_set.lego_set_id,
    #             price=result.get('price'),
    #             website_id=self.website_id
    #         )
    #     )
    #
    #     system_logger.info(f'Parse is end in {datetime.now() - time_start}')
    #
    #     return result
