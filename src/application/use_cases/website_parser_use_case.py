from abc import ABC, abstractmethod
import asyncio

import logging
from datetime import datetime

from application.interfaces.website_interface import WebsiteInterface
from application.repositories.prices_repository import LegoSetsPricesRepository
from domain.lego_sets_prices import LegoSetsPrices

system_logger = logging.getLogger('system_logger')


class WebsiteParserUseCase(ABC):
    @abstractmethod
    def parse_item(self):
        pass

    @abstractmethod
    def parse_items(self):
        pass

    async def _parse_items(self,
                           lego_sets: list,
                           website_interface: WebsiteInterface,
                           lego_sets_prices_repository: LegoSetsPricesRepository,
                           website_id: str):
        time_start=datetime.now()
        system_logger.info(f'Count Lego sets: {len(lego_sets)}')
        for i in range(0, len(lego_sets), 75):
            system_logger.info(f'Start parse sets from {i} bis {i+75}')
            # item_ids = [lego_set.lego_set_id for lego_set in lego_sets[i:i+75]]
            items_infos = await website_interface.parse_items(lego_sets=lego_sets[i:i+75])
            if items_infos is not None:
            # ic(results)
                for item_info in items_infos:
                    if item_info is not None:
                        lego_sets_prices = LegoSetsPrices(
                            lego_set_id=item_info.get('lego_set_id'),
                            prices={website_id: item_info.get('price')}
                        )
                        await self._save_new_price(
                            lego_sets_prices=lego_sets_prices,
                            lego_sets_prices_repository=lego_sets_prices_repository,
                            website_id=website_id
                        )

            system_logger.info(f'Start pause 15s')
            await asyncio.sleep(15)

        system_logger.info(f'Parse is end in {datetime.now()-time_start}')

    async def _save_new_price(self,
                               lego_sets_prices: LegoSetsPrices,
                               lego_sets_prices_repository: LegoSetsPricesRepository,
                               website_id: str,
                               ):

        if await lego_sets_prices_repository.get_item(item_id=lego_sets_prices.lego_set_id) is None:
            # Первое создание
            try:
                await lego_sets_prices_repository.add_item(
                    lego_sets_prices=lego_sets_prices
                )
                system_logger.info(f"Add new item successfully:\n"
                                   f"ID: {lego_sets_prices.lego_set_id} \n"
                                   f"Price: {lego_sets_prices.prices}\n"
                                   f"~~~~~~~~~~~~~~~~~~~~~~")

            except Exception as e:
                system_logger.error(f"Error by add new set with price: {e}")
        else:
            # Добавление цены
            print(f"item_price: {await lego_sets_prices_repository.get_item_price(item_id=lego_sets_prices.lego_set_id, website_id=website_id)}")
            try:
                await lego_sets_prices_repository.save_price(
                    item_id=lego_sets_prices.lego_set_id, website_id=website_id,
                    price=lego_sets_prices.prices.get(website_id)
                )
                system_logger.info(f"Save new items price successfully:\n"
                                   f"ID: {lego_sets_prices.lego_set_id} \n"
                                   f"Price: {lego_sets_prices.prices}\n"
                                   f"==================")
            except Exception as e:
                system_logger.error(f"Error by save new price: {e}")
