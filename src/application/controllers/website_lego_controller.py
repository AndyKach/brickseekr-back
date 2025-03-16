from application.controllers.website_controller import WebsiteController
from application.interfaces.website_data_source_interface import WebsiteDataSourceInterface
from application.interfaces.website_interface import WebsiteInterface
from application.interfaces.website_lego_interface import WebsiteLegoInterface
from application.repositories.legosets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from application.use_cases.website_lego_parser_use_case import WebsiteLegoParserUseCase
from infrastructure.config.logs_config import log_decorator


class WebsiteLegoController(WebsiteController):

    def __init__(self,
                 legosets_repository: LegoSetsRepository,
                 legosets_prices_repository: LegoSetsPricesRepository,
                 website_interface: WebsiteLegoInterface,
                 ):
        self.website_parser = WebsiteLegoParserUseCase(
            legosets_prices_repository=legosets_prices_repository,
            legosets_repository=legosets_repository,
            website_interface=website_interface
        )

    async def parse_legosets_price(self, legoset_id: str):
        await self.website_parser.parse_legosets_price(legoset_id=legoset_id)

    async def parse_legosets_prices(self):
        await self.website_parser.parse_legosets_prices()

    async def parse_legoset_images(self, legoset_id: str):
        await self.website_parser.parse_legoset_images(legoset_id=legoset_id)

    async def parse_legosets_images(self):
        await self.website_parser.parse_legosets_images()
