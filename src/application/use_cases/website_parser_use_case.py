from abc import ABC, abstractmethod
import asyncio

import logging
from datetime import datetime

from icecream import ic

from application.interfaces.website_interface import WebsiteInterface
from application.repositories.prices_repository import LegoSetsPricesRepository
from application.use_cases.lego_sets_prices_save_use_case import LegoSetsPricesSaveUseCase
from domain.legoset import LegoSet
from domain.legosets_price import LegoSetsPrice
from domain.legosets_prices import LegoSetsPrices

system_logger = logging.getLogger('system_logger')


class WebsiteParserUseCase(ABC):
    @abstractmethod
    def parse_legosets_price(self, legoset_id: str):
        pass

    @abstractmethod
    def parse_lego_sets_prices(self):
        pass

    @staticmethod
    async def _parse_items(
                           legosets: list[LegoSet],
                           website_interface: WebsiteInterface,
                           legosets_prices_save_use_case: LegoSetsPricesSaveUseCase,
                           website_id: int
                           ):
        time_start=datetime.now()
        count_valuable = 0
        system_logger.info(f'Count Lego sets: {len(legosets)}')
        for i in range(0, len(legosets), 75):
            system_logger.info(f'Start parse sets from {i} bis {i+75}')
            legosets_prices = await website_interface.parse_legosets_prices(lego_sets=legosets[i:i + 75])
            if legosets_prices is not None:
            # ic(results)
                for lego_set in legosets_prices:
                    if lego_set is not None:
                        count_valuable += 1
                        lego_sets_price = LegoSetsPrice(
                            legoset_id=lego_set.get('lego_set_id'),
                            price=lego_set.get('price'),
                            website_id=website_id
                        )
                        await legosets_prices_save_use_case.save_lego_sets_price(
                            legosets_price=lego_sets_price,

                        )

            system_logger.info(f'Start pause 15s')
            await asyncio.sleep(15)
        system_logger.info(f"Number of successful ones: {count_valuable}")
        system_logger.info(f'Parse is end in {datetime.now()-time_start}')

    @staticmethod
    async def _parse_item(
                          legoset: LegoSet,
                          website_interface: WebsiteInterface,
                          legosets_prices_save_use_case: LegoSetsPricesSaveUseCase,
                          website_id: int
                          ):
        result = await website_interface.parse_legosets_price(lego_set=legoset)
        system_logger.info(f"Lego set {legoset.legoset_id} - {result}")
        if result:
            await legosets_prices_save_use_case.save_lego_sets_price(
                LegoSetsPrice(
                    legoset_id=legoset.legoset_id,
                    price=result.get('price'),
                    website_id=website_id
                )
            )
        return result


