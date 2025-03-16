from application.controllers.website_controller import WebsiteController
from application.interfaces.website_interface import WebsiteInterface
from application.repositories.legosets_repository import LegosetsRepository
from application.repositories.prices_repository import LegosetsPricesRepository
from application.use_cases.website_kostickyshop_parser_use_case import WebsiteKostickyShopParserUseCase


class WebsiteKostikyShopController(WebsiteController):
    def __init__(self,
                 legosets_repository: LegosetsRepository,
                 legosets_prices_repository: LegosetsPricesRepository,
                 website_interface: WebsiteInterface,
                 ):
        self.website_parser_use_case = WebsiteKostickyShopParserUseCase(
            legosets_repository=legosets_repository,
            legosets_prices_repository=legosets_prices_repository,
            website_interface=website_interface
        )

    async def parse_legosets_prices(self):
        await self.website_parser_use_case.parse_legosets_prices()

    async def parse_legosets_price(self, legoset_id: str):
        await self.website_parser_use_case.parse_legosets_price(legoset_id=legoset_id)
