from application.controllers.website_controller import WebsiteController
from application.interfaces.website_interface import WebsiteInterface
from application.repositories.legosets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from application.use_cases.website_capi_cap_parser_use_case import WebsiteCapiCapParserUseCase


class WebsiteCapiCapController(WebsiteController):

    def __init__(self,
                 legosets_repository: LegoSetsRepository,
                 legosets_prices_repository: LegoSetsPricesRepository,
                 website_interface: WebsiteInterface,
                 ):
        self.website_parser_use_case = WebsiteCapiCapParserUseCase(
            legosets_repository=legosets_repository,
            legosets_prices_repository=legosets_prices_repository,
            website_interface=website_interface
        )

    async def parse_legosets_prices(self):
        await self.website_parser_use_case.parse_legosets_prices()

    async def parse_legosets_price(self, legoset_id: str):
        await self.website_parser_use_case.parse_legosets_price(legoset_id=legoset_id)
