from application.interfaces.website_interface import WebsiteInterface
from application.repositories.legosets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from application.use_cases.lego_sets_prices_save_use_case import LegoSetsPricesSaveUseCase
from application.use_cases.website_parser_use_case import WebsiteParserUseCase


class WebsiteKostickyShopParserUseCase(WebsiteParserUseCase):
    def __init__(self,
                 lego_sets_repository: LegoSetsRepository,
                 lego_sets_prices_repository: LegoSetsPricesRepository,
                 website_interface: WebsiteInterface,
                 ):
        self.legosets_repository = lego_sets_repository
        self.legosets_prices_repository = lego_sets_prices_repository
        self.website_interface = website_interface

        self.lego_sets_prices_save_use_case = LegoSetsPricesSaveUseCase(
            legosets_prices_repository=self.legosets_prices_repository
        )
        self.website_id = "5"


    async def parse_legosets_price(self, legoset_id: str):
        lego_set = await self.legosets_repository.get_set(set_id=legoset_id)
        await self._parse_item(
            legoset=lego_set,
            website_interface=self.website_interface,
            legosets_repository=self.legosets_repository,
            legosets_prices_save_use_case=self.lego_sets_prices_save_use_case,
            website_id=self.website_id
        )

    async def parse_legosets_prices(self):
        legosets = [legoset for legoset in await self.legosets_repository.get_all() if legoset.year > 2020]
        await self._parse_items(
            legosets=legosets,
            website_interface=self.website_interface,
            legosets_repository=self.legosets_repository,
            legosets_prices_save_use_case=self.lego_sets_prices_save_use_case,
            website_id=self.website_id
        )
