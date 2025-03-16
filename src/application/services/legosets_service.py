import asyncio
import logging
import time
from random import random

from icecream import ic

from application.controllers.website_brickset_controller import WebsiteBricksetController
from application.controllers.website_capi_cap_controller import WebsiteCapiCapController
from application.controllers.website_controller import WebsiteController
from application.controllers.website_kostickyshop_controller import WebsiteKostikyShopController
from application.controllers.website_lego_controller import WebsiteLegoController
from application.controllers.website_museum_of_bricks_controller import WebsiteMuseumOfBricksController
from application.controllers.website_sparkys_controller import WebsiteSparkysController
from application.interfaces.google_interface import GoogleInterface
from application.interfaces.parser_interface import ParserInterface
from application.interfaces.searchapi_interface import SearchAPIInterface
from application.interfaces.website_data_source_interface import WebsiteDataSourceInterface
from application.interfaces.website_interface import WebsiteInterface
from application.interfaces.website_lego_interface import WebsiteLegoInterface
from application.providers.websites_interfaces_provider import WebsitesInterfacesProvider
from application.repositories.legosets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from application.repositories.websites_repository import WebsitesRepository
from application.use_cases.get_legoset_price_use_case import GetLegoSetsPricesUseCase
from application.use_cases.get_legoset_use_case import GetLegoSetUseCase
from application.use_cases.legosets_rating_use_case import LegoSetsRatingUseCase
from application.use_cases.get_website_use_case import GetWebsiteUseCase
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
            websites_repository: WebsitesRepository,
            websites_interfaces_provider: WebsitesInterfacesProvider,
            search_api_interface: SearchAPIInterface,
            google_interface: GoogleInterface,
            ):
        self.legosets_repository = legosets_repository
        self.legosets_prices_repository = legosets_prices_repository
        self.websites_repository = websites_repository
        self.websites_interfaces_provider = websites_interfaces_provider
        self.google_interface = google_interface

        self.website_lego_controller = WebsiteLegoController(
            legosets_repository=legosets_repository,
            legosets_prices_repository=legosets_prices_repository,
            website_interface=self.website_lego_interface
        )
        self.website_capi_cap_controller = WebsiteCapiCapController(
            legosets_repository=legosets_repository,
            legosets_prices_repository=legosets_prices_repository,
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
        self.legosets_rating_use_case = LegoSetsRatingUseCase(
            legosets_repository=legosets_repository,
            legosets_prices_repository=legosets_prices_repository,
            search_api_interface=search_api_interface,
            google_interface=google_interface,
        )
        self.get_legosets_prices_use_case = GetLegoSetsPricesUseCase(
            legosets_prices_repository=legosets_prices_repository,
            website_lego_interface=self.website_lego_interface
        )
        self.get_website_use_case = GetWebsiteUseCase(
            websites_repository=websites_repository
        )

        self.get_legoset_use_case = GetLegoSetUseCase(
            legosets_repository=legosets_repository,
            legosets_prices_repository=legosets_prices_repository,
            websites_repository=websites_repository,
            website_brickset_controller=self.website_brickset_controller,
            get_legosets_rating_use_case=self.legosets_rating_use_case,
            get_legosets_prices_use_case=self.get_legosets_prices_use_case,
            get_website_use_case=self.get_website_use_case,
        )



    @property
    def website_lego_interface(self) -> WebsiteLegoInterface:
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

    async def get_legosets_rating_list(self, legosets_count: int):
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

    async def parse_set_in_store(self, set_id: str, store_id: str):
        website_controller = await self.__get_website_use_case(store_id=store_id)
        return await website_controller.parse_legosets_price(legoset_id=set_id)

    async def parse_all_sets_in_store(self, store_id: str):
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
        print('ITS TIME TO PARSE LEGO')
        # legosets = await self.legosets_repository.get_all()
        # await self.google_interface.open_driver()
        k = 0
        legosets_to_parse = []
        # try:
        #     for legoset in legosets:
        #         if len(legoset.images.keys()) == 2 and legoset.rating != 0:
        #             legosets_to_parse.append(legoset)
        #             if len(legosets_to_parse) >= 2000:
        #                 break
        #
        #     await self.website_lego_interface.parse_legosets_images(legosets=legosets_to_parse, legosets_repository=self.legosets_repository)
            # for legoset in legosets_to_parse:
            #     time.sleep(random()*10)
            #     before = legoset.rating
            #     result = await self.website_lego_interface.parse_legoset_images(legoset=legoset)
            #     # result = await self.get_legoset_use_case.execute(legoset_id=legoset.id)
            #     after = result.rating
            #     system_logger.info(f"Legoset: {legoset.id} RATING BEFORE: {before} AFTER: {after}")


        #     print('ITS TIME TO PARSE LEGO')
        # except Exception as e:
        #     system_logger.error(f"Error by parsing legosets ratings: {e}")
        # finally:
        #     pass
        #     # await self.google_interface.close_driver()

        # ic(lego_sets)

    async def parse_sets_from_brickset(self):
        return await self.website_brickset_controller.parse_legosets()

    async def parse_legoset_images(self, legoset_id: str):
        await self.website_lego_controller.parse_legoset_images(legoset_id=legoset_id)

    async def parse_legosets_images(self):
        await self.website_lego_controller.parse_legosets_images()

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legosets_from_lego(self):
        system_logger.warning('START')
        await self.website_lego_controller.parse_legosets()
        system_logger.warning('END')

    async def recalculate_rating(self):
        await self.legosets_rating_use_case.recalculate_all_legosets()
        # legosets = [legoset for legoset in await self.legosets_repository.get_all() if legoset.rating > 5]
        # system_logger.info(f"Count legosets to recalculate rating: {len(legosets)}")
        # for legoset in legosets:
        #     await self.get_legoset_use_case.execute(legoset_id=legoset.id)


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