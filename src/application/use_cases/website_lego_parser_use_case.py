import asyncio

from icecream import ic

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
            website_lego_interface: WebsiteInterface
    ):
        self.lego_sets_repository = lego_sets_repository
        self.lego_sets_prices_repository = lego_sets_prices_repository
        self.website_lego_interface = website_lego_interface

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
        item_info = await self.website_lego_interface.parse_item(item_id=lego_set_id)
        lego_sets_prices = LegoSetsPrices(
            lego_set_id=item_info.get('lego_set_id'),
            prices={'1': item_info.get('price')}
        )
        await self.__save_new_price(lego_sets_prices=lego_sets_prices)

    async def __parse_items(self, lego_sets: list):
        for i in range(0, len(lego_sets), 100):
            item_ids = [lego_set.lego_set_id for lego_set in lego_sets[i:i+100]]
            items_infos = await self.website_lego_interface.parse_items(item_ids=item_ids)
            # ic(results)
            for item_info in items_infos:
                if item_info is not None:
                    lego_sets_prices = LegoSetsPrices(
                        lego_set_id=item_info.get('lego_set_id'),
                        prices={'1': item_info.get('price')}
                    )
                    await self.__save_new_price(lego_sets_prices=lego_sets_prices)
            await asyncio.sleep(60)



    async def __save_new_price(self, lego_sets_prices: LegoSetsPrices):
        try:
            if await self.lego_sets_prices_repository.get_item_price(
                    item_id=lego_sets_prices.lego_set_id, website_id='1'
            ) is None:
                await self.lego_sets_prices_repository.add_item(lego_sets_prices=lego_sets_prices)
            else:
                await self.lego_sets_prices_repository.save_price(item_id=lego_sets_prices.lego_set_id, website_id='1',
                                                                  price=lego_sets_prices.prices.get('1'))
        except Exception as e:
            system_logger.error(e)