from application.interfaces.website_data_source_interface import WebsiteDataSourceInterface
from application.repositories.legosets_repository import LegoSetsRepository
from application.use_cases.website_parser_use_case import WebsiteParserUseCase


class WebsiteBricksetParserUseCase(WebsiteParserUseCase):
    def __init__(self,
                 website_interface: WebsiteDataSourceInterface,
                 legosets_repository: LegoSetsRepository
                 ):
        self.website_interface = website_interface
        self.legosets_repository = legosets_repository

    def parse_legosets_price(self, legoset_id: str):
        pass

    def parse_lego_sets_prices(self):
        pass

    #TODO доделать нормально
    async def parse_legoset(self, legoset_id: str):
        legoset = await self.website_interface.parse_legoset(legoset_id=legoset_id)

    async def parse_legosets(self):
        legosets = await self.website_interface.parse_all_legosets(legosets_repository=self.legosets_repository)
