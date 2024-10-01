import asyncio

from icecream import ic

from application.interfaces.parser_interface import ParserInterface
from application.interfaces.website_interface import WebsiteInterface
from application.providers.websites_interfaces_provider import WebsitesInterfacesProvider
from application.repositories.lego_sets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from application.use_cases.website_lego_parser_use_case import WebsiteLegoParserUseCase
from domain.lego_sets_prices import LegoSetsPrices
from infrastructure.config.logs_config import system_logger


class LegoSetsService:
    def __init__(
            self,
            lego_sets_repository: LegoSetsRepository,
            lego_sets_prices_repository: LegoSetsPricesRepository,
            websites_interfaces_provider: WebsitesInterfacesProvider,
            ):
        self.lego_sets_repository = lego_sets_repository
        self.lego_sets_prices_repository = lego_sets_prices_repository
        self.websites_interfaces_provider = websites_interfaces_provider

        self.website_lego_parser_use_case = WebsiteLegoParserUseCase(
            lego_sets_repository=lego_sets_repository,
            lego_sets_prices_repository=lego_sets_prices_repository,
            website_lego_interface=self.website_lego_interface
        )

    @property
    def website_lego_interface(self) -> WebsiteInterface:
        return self.websites_interfaces_provider.get_website_lego_interface()

    async def get_set_info(self, set_id: str):
        return await self.lego_sets_repository.get_set(set_id=set_id)

    # async def parse_all_sets(self):
    #     lego_sets = await self.lego_sets_repository.get_all()
    #     ic('Start parsing lego sets')
    #     for lego_set in lego_sets[-10:]:
    #         ic(lego_set)
    #         item_price = await self.lego_parser_interface.parse_item(item_id=lego_set.lego_set_id)
    #         if item_price:
    #             # system_logger.info(f'Lego set {lego_set.lego_set_id} exists, price: {item_price}')
    #             lego_sets_prices = LegoSetsPrices(
    #                 lego_set_id=lego_set.lego_set_id,
    #                 prices={'1': item_price}
    #             )
    #             try:
    #                 await self.lego_sets_prices_repository.add_item(
    #                     lego_sets_prices=lego_sets_prices
    #                 )
    #             except Exception as e:
    #                 ic(e)
    #         else:
    #             pass
    #             system_logger.info(f'Lego set {lego_set.lego_set_id} not exists')

    async def async_parse_all_known_sets(self):
        await self.website_lego_parser_use_case.parse_known_sets()
        # lego_sets = await self.lego_sets_prices_repository.get_all_items()

    async def async_parse_all_unknown_sets(self):
        await self.website_lego_parser_use_case.parse_known_sets()

    async def get_sets_prices(self, set_id: str):
        lego_sets_prices = await self.lego_sets_prices_repository.get_item_all_prices(item_id=set_id)
        result = {
            "set_id": set_id,
            "prices": lego_sets_prices
        }
        return result

    async def get_sets_prices_from_website(self, set_id: str, website_id: str):
        lego_sets_price = await self.lego_sets_prices_repository.get_item_price(item_id=set_id, website_id=website_id)
        result = {
            "set_id": set_id,
            "website_id": website_id,
            "price": lego_sets_price
        }
        return result



        # ic(lego_sets)