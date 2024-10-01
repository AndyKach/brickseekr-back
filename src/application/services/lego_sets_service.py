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

    async def async_parse_set(self, set_id: str):
        await self.website_lego_parser_use_case.parse_set(lego_set_id=set_id)

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

    async def tmp_function(self):
        print('ITS TIME TO PARSE LEGO')
        # ic(lego_sets)