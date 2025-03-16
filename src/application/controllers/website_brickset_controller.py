from application.interfaces.website_brickset_interface import WebsiteBrickSetInterface
from application.interfaces.website_data_source_interface import WebsiteDataSourceInterface
from application.repositories.legosets_repository import LegosetsRepository
from application.use_cases.website_brickset_parser_use_case import WebsiteBricksetParserUseCase


class WebsiteBricksetController:
    def __init__(self,
                 website_interface: WebsiteBrickSetInterface,
                 legosets_repository: LegosetsRepository,
                 ):
        self.brickset_parser_use_case = WebsiteBricksetParserUseCase(
            website_interface=website_interface,
            legosets_repository=legosets_repository
        )

    async def parse_legoset(self, legoset_id: str):
        pass

    async def parse_legosets(self):
        await self.brickset_parser_use_case.parse_legosets()

