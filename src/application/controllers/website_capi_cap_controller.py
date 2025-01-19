from application.controllers.website_controller import WebsiteController
from application.interfaces.website_interface import WebsiteInterface
from application.repositories.legosets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from application.use_cases.website_capi_cap_parser_use_case import WebsiteCapiCapParserUseCase


class WebsiteCapiCapController(WebsiteController):

    def __init__(self,
                 lego_sets_repository: LegoSetsRepository,
                 lego_sets_prices_repository: LegoSetsPricesRepository,
                 website_interface: WebsiteInterface,
                 ):
        self.lego_sets_repository = lego_sets_repository,
        self.lego_sets_prices_repository = lego_sets_prices_repository,
        self.website_interface = website_interface

        self.website_parser_use_case = WebsiteCapiCapParserUseCase(
            lego_sets_repository=lego_sets_repository,
            lego_sets_prices_repository=lego_sets_prices_repository,
            website_interface=self.website_interface
        )

    async def parse_lego_sets_prices(self):
        await self.website_parser_use_case.parse_lego_sets_prices()

    async def parse_lego_sets_price(self, lego_set_id: str):
        return await self.website_parser_use_case.parse_lego_sets_price(lego_set_id=lego_set_id)
