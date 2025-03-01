import asyncio
import logging
from icecream import ic

from application.controllers.website_brickset_controller import WebsiteBricksetController
from application.controllers.website_capi_cap_controller import WebsiteCapiCapController
from application.controllers.website_controller import WebsiteController
from application.controllers.website_kostickyshop_controller import WebsiteKostikyShopController
from application.controllers.website_lego_controller import WebsiteLegoController
from application.controllers.website_museum_of_bricks_controller import WebsiteMuseumOfBricksController
from application.controllers.website_sparkys_controller import WebsiteSparkysController
from application.interfaces.parser_interface import ParserInterface
from application.interfaces.searchapi_interface import SearchAPIInterface
from application.interfaces.website_data_source_interface import WebsiteDataSourceInterface
from application.interfaces.website_interface import WebsiteInterface
from application.providers.websites_interfaces_provider import WebsitesInterfacesProvider
from application.repositories.legosets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from application.use_cases.get_legoset_price_use_case import GetLegoSetPriceUseCase
from application.use_cases.get_legoset_use_case import GetLegoSetUseCase
from application.use_cases.get_legosets_rating_use_case import GetLegoSetsRatingUseCase
from application.use_cases.website_capi_cap_parser_use_case import WebsiteCapiCapParserUseCase
from application.use_cases.website_lego_parser_use_case import WebsiteLegoParserUseCase
from application.use_cases.website_museum_of_bricks_parser_use_case import WebsiteMuseumOfBricksParserUseCase
from application.use_cases.website_parser_use_case import WebsiteParserUseCase
from domain.legosets_prices import LegoSetsPrices
from infrastructure.config.logs_config import log_decorator

system_logger = logging.getLogger('system_logger')
class LegoSetsService:
    def __init__(
            self,
            legosets_repository: LegoSetsRepository,
            legosets_prices_repository: LegoSetsPricesRepository,
            websites_interfaces_provider: WebsitesInterfacesProvider,
            search_api_interface: SearchAPIInterface,
            ):
        self.legosets_repository = legosets_repository
        self.legosets_prices_repository = legosets_prices_repository
        self.websites_interfaces_provider = websites_interfaces_provider

        self.website_lego_controller = WebsiteLegoController(
            legosets_repository=legosets_repository,
            legosets_prices_repository=legosets_prices_repository,
            website_interface=self.website_lego_interface
        )
        self.website_capi_cap_controller = WebsiteCapiCapController(
            lego_sets_repository=legosets_repository,
            lego_sets_prices_repository=legosets_prices_repository,
            website_interface=self.website_capi_cap_interface
        )
        self.website_museum_of_bricks_controller = WebsiteMuseumOfBricksController(
            lego_sets_repository=legosets_repository,
            lego_sets_prices_repository=legosets_prices_repository,
            website_interface=self.website_museum_of_bricks_interface
        )
        self.website_sparkys_controller = WebsiteSparkysController(
            lego_sets_repository=legosets_repository,
            lego_sets_prices_repository=legosets_prices_repository,
            website_interface=self.website_sparkys_interface
        )
        self.website_kostickyshop_controller = WebsiteKostikyShopController(
            lego_sets_repository=legosets_repository,
            lego_sets_prices_repository=legosets_prices_repository,
            website_interface=self.website_kostickyshop_interface
        )
        self.website_brickset_controller = WebsiteBricksetController(
            website_interface=self.website_brickset_interface,
            legosets_repository=legosets_repository
        )
        self.get_legosets_rating_use_case = GetLegoSetsRatingUseCase(
            legosets_repository=legosets_repository,
            legosets_prices_repository=legosets_prices_repository,
            search_api_interface=search_api_interface,
            website_lego_interface=self.website_lego_interface
        )
        self.get_legoset_use_case = GetLegoSetUseCase(
            legosets_repository=legosets_repository,
            legosets_prices_repository=legosets_prices_repository,
            website_brickset_controller=self.website_brickset_controller,
            get_legosets_rating_use_case=self.get_legosets_rating_use_case,
        )
        self.get_legoset_prices_use_case = GetLegoSetPriceUseCase(
            legosets_prices_repository=legosets_prices_repository,
            website_lego_interface=self.website_lego_interface
        )



    @property
    def website_lego_interface(self) -> WebsiteDataSourceInterface:
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

    async def get_legoset_info(self, legoset_id: str):
        return await self.get_legoset_use_case.execute(legoset_id=legoset_id)

    async def get_sets_prices(self, set_id: str):
        return await self.get_legoset_prices_use_case.get_all_prices(legoset_id=set_id)
        # return await self.legosets_prices_repository.get_item_all_prices(lego_set_id=set_id)

    async def get_sets_prices_from_website(self, set_id: str, website_id: str):
        return await self.get_legoset_prices_use_case.get_website_price(legoset_id=set_id, website_id=website_id,
                                                                        website_controller=await self.__get_website_use_case(website_id))
        # return await self.legosets_prices_repository.get_item_price(lego_set_id=set_id, website_id=website_id)

    async def get_legoset_from_lego_website(self, legoset_id: str):
        lego_website_controller = await self.__get_website_use_case(store_id=1)
        await lego_website_controller.parse_legosets_price(legoset_id=legoset_id)

    async def get_legosets_rating_list(self, legosets_count: int = 20):
        return await self.get_legoset_use_case.get_top_list(legosets_count=legosets_count)

    async def async_parse_sets(self, store: str):
        website_controller = await self.__get_website_use_case(store=store)
        print(website_controller)
        await website_controller.parse_legosets_prices()

    async def parse_lego_sets_url(self):
        await self.website_museum_of_bricks_controller.parse_lego_sets_url()

    async def parse_lego_sets_urls(self):
        await self.website_museum_of_bricks_controller.parse_lego_sets_urls()


    async def async_parse_set(self, set_id: str):
        await self.website_lego_controller.parse_set(lego_set_id=set_id)

    async def parse_set_in_store(self, set_id: str, store_id: int):
        website_controller = await self.__get_website_use_case(store_id=store_id)
        return await website_controller.parse_legosets_price(legoset_id=set_id)

    async def parse_all_sets_in_store(self, store_id: int):
        website_controller = await self.__get_website_use_case(store_id=store_id)
        await website_controller.parse_legosets_prices()

    # async def async_parse_all_known_sets(self):
    #     await self.website_lego_controller.parse_known_sets()
    #
    # async def async_parse_all_unknown_sets(self):
    #     await self.website_lego_controller.parse_all_sets()

    # async def get_legosets_rating(self, legoset_id: str):
    #     return await self.get_legosets_rating_use_case.execute(legoset_id=legoset_id)

    async def tmp_function(self):
        legosets = await self.legosets_repository.get_all()
        k = 0
        legosets_to_parse = []
        for legoset in legosets:
            if legoset.rating is None:
                legosets_to_parse.append(legoset)
                if len(legosets_to_parse) >= 2:
                    break

        for legoset in legosets_to_parse:
            before = legoset.rating
            result = await self.get_legoset_use_case.execute(legoset_id=legoset.id)
            after = result.rating
            system_logger.info(f"Legoset: {legoset.id} RATING BEFORE: {before} AFTER: {after}`")


        print('ITS TIME TO PARSE LEGO')
        # ic(lego_sets)

    async def parse_sets_from_brickset(self):
        return await self.website_brickset_controller.parse_legosets()

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legosets_from_lego(self):
        system_logger.warning('START')
        await self.website_lego_controller.parse_legosets()
        system_logger.warning('END')



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