from abc import ABC, abstractmethod
import asyncio

import logging
from datetime import datetime

from icecream import ic

from application.interfaces.website_interface import WebsiteInterface
from application.repositories.prices_repository import LegoSetsPricesRepository
from application.use_cases.lego_sets_prices_save_use_case import LegoSetsPricesSaveUseCase
from domain.lego_set import LegoSet
from domain.lego_sets_price import LegoSetsPrice
from domain.lego_sets_prices import LegoSetsPrices

system_logger = logging.getLogger('system_logger')


class WebsiteParserUseCase(ABC):
    @abstractmethod
    def parse_lego_sets_price(self, lego_set_id: str):
        pass

    @abstractmethod
    def parse_lego_sets_prices(self):
        pass

    @staticmethod
    async def _parse_items(
                           lego_sets: list[LegoSet],
                           website_interface: WebsiteInterface,
                           lego_sets_prices_save_use_case: LegoSetsPricesSaveUseCase,
                           website_id: str
                           ):
        time_start=datetime.now()
        count_valuable = 0
        system_logger.info(f'Count Lego sets: {len(lego_sets)}')
        for i in range(0, len(lego_sets), 75):
            system_logger.info(f'Start parse sets from {i} bis {i+75}')
            lego_sets_prices = await website_interface.parse_lego_sets_prices(lego_sets=lego_sets[i:i + 75])
            if lego_sets_prices is not None:
            # ic(results)
                for lego_set in lego_sets_prices:
                    if lego_set is not None:
                        count_valuable += 1
                        lego_sets_price = LegoSetsPrice(
                            lego_set_id=lego_set.get('lego_set_id'),
                            price=lego_set.get('price'),
                            website_id=website_id
                        )
                        await lego_sets_prices_save_use_case.save_lego_sets_price(
                            lego_sets_price=lego_sets_price,

                        )

            system_logger.info(f'Start pause 15s')
            await asyncio.sleep(15)
        system_logger.info(f"Number of successful ones: {count_valuable}")
        system_logger.info(f'Parse is end in {datetime.now()-time_start}')

    @staticmethod
    async def _parse_item(
                          lego_set: LegoSet,
                          website_interface: WebsiteInterface,
                          lego_sets_prices_save_use_case: LegoSetsPricesSaveUseCase,
                          website_id: str
                          ):
        result = await website_interface.parse_lego_sets_price(lego_set=lego_set)
        system_logger.info(f"Lego set {lego_set.lego_set_id} - {result}")
        await lego_sets_prices_save_use_case.save_lego_sets_price(
            LegoSetsPrice(
                lego_set_id=lego_set.lego_set_id,
                price=result.get('price'),
                website_id=website_id
            )
        )
        return result


