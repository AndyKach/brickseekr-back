import asyncio

from icecream import ic

from application.controllers.website_capi_cap_controller import WebsiteCapiCapController
from application.controllers.website_controller import WebsiteController
from application.controllers.website_kostickyshop_controller import WebsiteKostikyShopController
from application.controllers.website_lego_controller import WebsiteLegoController
from application.controllers.website_museum_of_bricks_controller import WebsiteMuseumOfBricksController
from application.controllers.website_sparkys_controller import WebsiteSparkysController
from application.interfaces.parser_interface import ParserInterface
from application.interfaces.website_data_source_interface import WebsiteDataSourceInterface
from application.interfaces.website_interface import WebsiteInterface
from application.providers.websites_interfaces_provider import WebsitesInterfacesProvider
from application.repositories.lego_sets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from application.use_cases.get_legoset_use_case import GetLegoSetUseCase
from application.use_cases.website_capi_cap_parser_use_case import WebsiteCapiCapParserUseCase
from application.use_cases.website_lego_parser_use_case import WebsiteLegoParserUseCase
from application.use_cases.website_museum_of_bricks_parser_use_case import WebsiteMuseumOfBricksParserUseCase
from application.use_cases.website_parser_use_case import WebsiteParserUseCase
from domain.legosets_prices import LegoSetsPrices


class LegoSetsService:
    def __init__(
            self,
            legosets_repository: LegoSetsRepository,
            lego_sets_prices_repository: LegoSetsPricesRepository,
            websites_interfaces_provider: WebsitesInterfacesProvider,
            ):
        self.lego_sets_repository = legosets_repository
        self.lego_sets_prices_repository = lego_sets_prices_repository
        self.websites_interfaces_provider = websites_interfaces_provider

        self.website_lego_controller = WebsiteLegoController(
            lego_sets_repository=legosets_repository,
            lego_sets_prices_repository=lego_sets_prices_repository,
            website_interface=self.website_lego_interface
        )
        self.website_capi_cap_controller = WebsiteCapiCapController(
            lego_sets_repository=legosets_repository,
            lego_sets_prices_repository=lego_sets_prices_repository,
            website_interface=self.website_capi_cap_interface
        )
        self.website_museum_of_bricks_controller = WebsiteMuseumOfBricksController(
            lego_sets_repository=legosets_repository,
            lego_sets_prices_repository=lego_sets_prices_repository,
            website_interface=self.website_museum_of_bricks_interface
        )
        self.website_sparkys_controller = WebsiteSparkysController(
            lego_sets_repository=legosets_repository,
            lego_sets_prices_repository=lego_sets_prices_repository,
            website_interface=self.website_sparkys_interface
        )
        self.website_kostickyshop_controller = WebsiteKostikyShopController(
            lego_sets_repository=legosets_repository,
            lego_sets_prices_repository=lego_sets_prices_repository,
            website_interface=self.website_kostickyshop_interface
        )
        self.get_legoset_use_case = GetLegoSetUseCase(
            legosets_repository=legosets_repository,
        )


    @property
    def website_lego_interface(self) -> WebsiteInterface:
        return self.websites_interfaces_provider.get_website_lego_interface()

    @property
    def website_capi_cap_interface(self) -> WebsiteInterface:
        return self.websites_interfaces_provider.get_website_capi_cap_interface()

    @property
    def website_museum_of_bricks_interface(self) -> WebsiteInterface:
        return self.websites_interfaces_provider.get_website_museum_of_bricks_interface()
    
    @property
    def website_sparkys_interface(self) -> WebsiteInterface:
        return self.websites_interfaces_provider.get_website_sparkys_interface()

    @property
    def website_kostickyshop_interface(self) -> WebsiteInterface:
        return self.websites_interfaces_provider.get_website_kostickyshop_interface()

    @property
    def website_brickset_interface(self) -> WebsiteDataSourceInterface:
        return self.websites_interfaces_provider.get_website_brickset_interface()

    async def get_set_info(self, set_id: str):
        return await self.get_legoset_use_case.execute(legoset_id=set_id)

    async def async_parse_sets(self, store: str):
        website_controller = await self.__get_website_use_case(store=store)
        print(website_controller)
        await website_controller.parse_lego_sets_prices()

    async def parse_lego_sets_url(self):
        await self.website_museum_of_bricks_controller.parse_lego_sets_url()

    async def parse_lego_sets_urls(self):
        await self.website_museum_of_bricks_controller.parse_lego_sets_urls()


    async def async_parse_set(self, set_id: str):
        await self.website_lego_controller.parse_set(lego_set_id=set_id)

    async def parse_set_in_store(self, set_id: str, store_id: str):
        website_controller = await self.__get_website_use_case(store_id=store_id)
        return await website_controller.parse_lego_sets_price(lego_set_id=set_id)

    async def parse_all_sets_in_store(self, store_id: str):
        website_controller = await self.__get_website_use_case(store_id=store_id)
        await website_controller.parse_lego_sets_prices()

    async def async_parse_all_known_sets(self):
        await self.website_lego_controller.parse_known_sets()

    async def async_parse_all_unknown_sets(self):
        await self.website_lego_controller.parse_all_sets()

    async def get_sets_prices(self, set_id: str):
        return await self.lego_sets_prices_repository.get_item_all_prices(lego_set_id=set_id)

    async def get_sets_prices_from_website(self, set_id: str, website_id: str):
        return await self.lego_sets_prices_repository.get_item_price(lego_set_id=set_id, website_id=website_id)

    async def tmp_function(self):
        print('ITS TIME TO PARSE LEGO')
        # ic(lego_sets)

    async def parse_sets_from_brickset(self):
        await self.website_brickset_interface.parse_all_legosets()

    async def __get_website_use_case(self, store_id: str) -> WebsiteController:
        match store_id:
            case "1":
                return self.website_lego_controller
            case "2":
                return self.website_capi_cap_controller
            case "3":
                return self.website_sparkys_controller
            case "4":
                return self.website_museum_of_bricks_controller
            case "5":
                return self.website_kostickyshop_controller