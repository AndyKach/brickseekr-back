import asyncio

from icecream import ic

from application.interfaces.website_interface import WebsiteInterface
from application.repositories.lego_sets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from domain.lego_set import LegoSet
from domain.lego_sets_prices import LegoSetsPrices
from infrastructure.config.logs_config import log_decorator


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
        print(lego_sets)
        await self.parse(lego_sets=lego_sets)

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_all_sets(self):
        """
        Parse sets from lego_sets
        """
        lego_sets = await self.lego_sets_repository.get_all()
        await self.parse(lego_sets=lego_sets)

    async def parse(self, lego_sets: list):
        for i in range(0, len(lego_sets), 500):
            item_ids = [lego_set.lego_set_id for lego_set in lego_sets[i:i+500]]
            results = await self.website_lego_interface.parse_items(item_ids=item_ids)
            # ic(results)
            for result in results:
                if result is not None:
                    lego_sets_prices = LegoSetsPrices(
                        lego_set_id=result.get('lego_set_id'),
                        prices={'1': result.get('price')}
                    )
                    try:
                        await self.lego_sets_prices_repository.add_item(
                            lego_sets_prices=lego_sets_prices
                        )
                    except Exception as e:
                        ic(e)
            await asyncio.sleep(60)