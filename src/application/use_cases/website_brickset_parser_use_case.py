from application.interfaces.website_data_source_interface import WebsiteDataSourceInterface
from application.use_cases.website_parser_use_case import WebsiteParserUseCase


class WebsiteBricksetParserUseCase(WebsiteParserUseCase):
    def __init__(self,
                 website_brickset_interface: WebsiteDataSourceInterface
                 ):
        self.website_brickset_interface = website_brickset_interface

    def parse_legosets_price(self, legoset_id: str):
        pass

    def parse_lego_sets_prices(self):
        pass

    async def parse_legoset(self, legoset_id: str):
        legoset = await self.website_brickset_interface.parse_legoset(legoset_id=legoset_id)
