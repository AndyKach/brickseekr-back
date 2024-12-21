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
from infrastructure.config.logs_config import log_decorator, system_logger


class WebsiteLegoParserUseCase(WebsiteParserUseCase):
    def __init__(
            self,
            lego_sets_prices_repository: LegoSetsPricesRepository,
            lego_sets_repository: LegoSetsRepository,
            website_lego_interface: WebsiteInterface
    ):
        self.lego_sets_repository = lego_sets_repository
        self.lego_sets_prices_repository = lego_sets_prices_repository
        self.website_lego_interface = website_lego_interface

    async def parse_item(self):
        pass

    async def parse_items(self):
        pass

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_known_sets(self):
        """
        Parse sets from lego_sets_prices
        """
        lego_sets = await self.lego_sets_prices_repository.get_all_items()
        # print(lego_sets)
        await self.__parse_items(lego_sets=lego_sets)


    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_all_sets(self):
        """
        Parse sets from lego_sets
        """
        lego_sets = await self.lego_sets_repository.get_all()
        await self.__parse_items(lego_sets=lego_sets)

    async def parse_set(self, lego_set_id: str):
        await self.__parse_item(lego_set_id=lego_set_id)

    async def __parse_item(self, lego_set_id: str):
        time_start=datetime.now()

        item_info = await self.website_lego_interface.parse_item(item_id=lego_set_id)
        if item_info is not None:
            lego_sets_prices = LegoSetsPrices(
                lego_set_id=item_info.get('lego_set_id'),
                prices={'1': item_info.get('price')}
            )
            await self.__save_new_price(lego_sets_prices=lego_sets_prices)

        system_logger.info(f'Parse is end in {datetime.now()-time_start}')


    async def __parse_items(self, lego_sets: list):
        time_start=datetime.now()
        system_logger.info(f'Count Lego sets: {len(lego_sets)}')
        for i in range(0, len(lego_sets), 75):
            system_logger.info(f'Start parse sets from {i} bis {i+75}')
        # for i in range(, 100, 100):
            item_ids = [lego_set.lego_set_id for lego_set in lego_sets[i:i+75]]
            items_infos = await self.website_lego_interface.parse_items(item_ids=item_ids)
            if items_infos is not None:
            # ic(results)
                for item_info in items_infos:
                    if item_info is not None:
                        lego_sets_prices = LegoSetsPrices(
                            lego_set_id=item_info.get('lego_set_id'),
                            prices={'1': item_info.get('price')}
                        )
                        await self.__save_new_price(lego_sets_prices=lego_sets_prices)

            system_logger.info(f'Start pause 15s')
            await asyncio.sleep(15)

        system_logger.info(f'Parse is end in {datetime.now()-time_start}')



    async def __save_new_price(self, lego_sets_prices: LegoSetsPrices):
        if await self.lego_sets_prices_repository.get_item_price(
                item_id=lego_sets_prices.lego_set_id, website_id='1'
        ) is None:
            try:
                await self.lego_sets_prices_repository.add_item(
                    lego_sets_prices=lego_sets_prices
                )
                system_logger.info(f"Add new item successfully:\nID: {lego_sets_prices.lego_set_id} \nPrice: {lego_sets_prices.prices}")

            except Exception as e:
                system_logger.error(f"Error by add new set with price: {e}")
        else:
            try:
                await self.lego_sets_prices_repository.save_price(
                    item_id=lego_sets_prices.lego_set_id, website_id='1',
                    price=lego_sets_prices.prices.get('1')
                )
                system_logger.info(f"Save new item successfully:\nID: {lego_sets_prices.lego_set_id} \nPrice: {lego_sets_prices.prices}")
            except Exception as e:
                system_logger.error(f"Error by save new price: {e}")
