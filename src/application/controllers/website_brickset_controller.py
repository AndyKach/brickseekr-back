from application.controllers.website_controller import WebsiteController
from application.interfaces.website_data_source_interface import WebsiteDataSourceInterface
from application.repositories.legosets_repository import LegoSetsRepository
from application.use_cases.website_brickset_parser_use_case import WebsiteBricksetParserUseCase


class WebsiteBricksetController(WebsiteController):
    def __init__(self,
                 website_interface: WebsiteDataSourceInterface,
                 legosets_repository: LegoSetsRepository,
                 ):
        self.website_interface = website_interface
        self.legosets_repository = legosets_repository
        self.brickset_parser_use_case = WebsiteBricksetParserUseCase(
            website_interface=self.website_interface,
            legosets_repository=legosets_repository
        )

    async def parse_legosets_prices(self):
        pass

    async def parse_legosets_price(self, legoset_id: str):
        pass

    async def parse_legoset(self, legoset_id: str):
        pass

    async def parse_legosets(self):
        await self.brickset_parser_use_case.parse_legosets()

