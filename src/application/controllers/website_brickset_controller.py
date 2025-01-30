from application.controllers.website_controller import WebsiteController
from application.use_cases.website_brickset_parser_use_case import WebsiteBricksetParserUseCase


class WebsiteBricksetController(WebsiteController):
    def __init__(self):
        self.brickset_parser_use_case = WebsiteBricksetParserUseCase()

    async def parse_legosets_prices(self):
        pass

    async def parse_legosets_price(self, legoset_id: str):
        pass

    async def parse_legoset(self, legoset_id: str):
        pass
