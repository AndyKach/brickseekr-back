from abc import ABC, abstractmethod
import asyncio

import logging
from datetime import datetime

from icecream import ic

from application.interfaces.website_interface import WebsiteInterface
from application.repositories.prices_repository import LegoSetsPricesRepository
from application.repositories.legosets_repository import LegoSetsRepository
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
    def parse_legosets_prices(self):
        pass

    @staticmethod
    async def _parse_items(
            legosets: list[LegoSet],
            website_interface: WebsiteInterface,
            legosets_prices_save_use_case: LegoSetsPricesSaveUseCase,
            legosets_repository: LegoSetsRepository,
            website_id: str):
        time_start=datetime.now()
        count_valuable = 0
        system_logger.info(f'Count Lego sets: {len(legosets)}')
        for i in range(0, len(legosets), 50):
            system_logger.info(f'Start parse sets from {i} bis {i+50}')
            results = await website_interface.parse_legosets_prices(legosets=legosets[i:i + 50])
            if results:
                ic(results)
                for result in results:
                    try:
                        if result:
                            count_valuable += 1
                            if result.get('available') == "Retired product":
                                await legosets_prices_save_use_case.delete_legosets_price(legoset_id=result.get('legoset_id'), website_id=website_id)
                            if result.get('price'):
                                await legosets_prices_save_use_case.save_legosets_price(
                                    LegoSetsPrice(
                                        legoset_id=result.get('legoset_id'),
                                        price=result.get('price'),
                                        website_id=website_id
                                            )
                                        )
                            # Needed to be deleted dann
                            # legoset = await legosets_repository.get_set(set_id=result.get('legoset_id'))
                            # for i in range(1, 6):
                            #     if result.get(f'small_image{i}'):
                            #         legoset.images[f'small_image{i}'] = result.get(f'small_image{i}')
                            #     if result.get(f'big_image{i}'):
                            #         legoset.images[f'big_image{i}'] = result.get(f'big_image{i}')
                            #     await legosets_repository.update_set(legoset=legoset)
                    except Exception as e:
                        system_logger.error(e)

            system_logger.info(f'Start pause 15s')
            await asyncio.sleep(15)
        system_logger.info(f"Number of successful ones: {count_valuable}")
        system_logger.info(f'Parse is end in {datetime.now()-time_start}')

    @staticmethod
    async def _parse_item(
                          legoset: LegoSet,
                          website_interface: WebsiteInterface,
                          legosets_prices_save_use_case: LegoSetsPricesSaveUseCase,
                          legosets_repository: LegoSetsRepository,
                          website_id: str
                          ):

        result = await website_interface.parse_legosets_price(legoset=legoset)
        system_logger.info(f"Lego set {legoset.id} - {result}")
        if result:
            # return None
            if result.get('available') == "Retired product":
                await legosets_prices_save_use_case.delete_legosets_price(legoset_id=legoset.id, website_id=website_id)
            if result.get('price'):
                await legosets_prices_save_use_case.save_legosets_price(
                    LegoSetsPrice(
                        legoset_id=legoset.id,
                        price=result.get('price'),
                        website_id=website_id
                    )
                )











            # Needed to be deleted dann
            # for i in range(1, 6):
            #     if result.get(f'small_image{i}'):
            #         legoset.images[f'small_image{i}'] = result.get(f'small_image{i}')
            #     if result.get(f'big_image{i}'):
            #         legoset.images[f'big_image{i}'] = result.get(f'big_image{i}')
            #     await legosets_repository.update_set(legoset=legoset)

        return result


