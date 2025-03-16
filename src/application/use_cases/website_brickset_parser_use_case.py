from application.interfaces.website_brickset_interface import WebsiteBrickSetInterface
from application.repositories.legosets_repository import LegosetsRepository
from application.use_cases.website_parser_use_case import WebsiteParserUseCase
from domain.legoset import Legoset


class WebsiteBricksetParserUseCase(WebsiteParserUseCase):
    def __init__(self,
                 website_interface: WebsiteBrickSetInterface,
                 legosets_repository: LegosetsRepository
                 ):
        self.website_interface = website_interface
        self.legosets_repository = legosets_repository

    def parse_legosets_price(self, legoset_id: str):
        pass

    def parse_legosets_prices(self):
        pass

    async def parse_legoset(self, legoset_id: str):
        legoset = await self.website_interface.parse_legoset(legoset_id=legoset_id)

    async def parse_legosets(self):
        legosets = await self.website_interface.parse_legosets(legosets_repository=self.legosets_repository)
