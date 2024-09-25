from icecream import ic
from watchfiles import awatch

from application.interfaces.parser_interface import ParserInterface
from application.repositories.lego_sets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from domain.lego_sets_prices import LegoSetsPrices
from infrastructure.config.logs_config import system_logger


class LegoSetsService:
    def __init__(
            self,
            lego_sets_repository: LegoSetsRepository,
            lego_sets_prices_repository: LegoSetsPricesRepository,
            lego_parser_interface: ParserInterface,
            ):
        self.lego_sets_repository = lego_sets_repository
        self.lego_sets_prices_repository = lego_sets_prices_repository
        self.lego_parser_interface = lego_parser_interface

    async def get_set_info(self, set_id: str):
        return await self.lego_sets_repository.get_set(set_id=set_id)

    async def parse_all_sets(self):
        lego_sets = await self.lego_sets_repository.get_all()
        ic('Start parsing lego sets')
        for lego_set in lego_sets[-10:]:
            ic(lego_set)
            item_price = await self.lego_parser_interface.parse_item(item_id=lego_set.lego_set_id)
            if item_price:
                system_logger.info(f'Lego set {lego_set.lego_set_id} exists, price: {item_price}')
                lego_sets_prices = LegoSetsPrices(
                    lego_set_id=lego_set.lego_set_id,
                    prices={'1': item_price}
                )
                # await self.lego_sets_prices_repository.save_price(
                #     item_id=lego_set.lego_set_id,
                #     website_id='2',
                #     price=item_price
                # )
                try:
                    await self.lego_sets_prices_repository.add_item(
                        lego_sets_prices=lego_sets_prices
                    )
                except Exception as e:
                    ic(e)
            else:
                system_logger.info(f'Lego set {lego_set.lego_set_id} not exists')

    async def async_parse_all_sets(self):
        lego_sets = await self.lego_sets_repository.get_all()
        ic('Start parsing lego sets')

        item_ids = [lego_set.lego_set_id for lego_set in lego_sets[:]]
        print(item_ids)
        await self.lego_parser_interface.parse_items(item_ids=item_ids)





        return True


        # ic(lego_sets)