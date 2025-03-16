from application.interfaces.website_data_source_interface import WebsiteDataSourceInterface
from application.interfaces.website_interface import WebsiteInterface
from abc import ABC, abstractmethod

from domain.legoset import Legoset


class WebsiteLegoInterface(WebsiteInterface):
    @abstractmethod
    async def parse_legosets_price(self, legoset: Legoset) -> dict:
        pass

    @abstractmethod
    async def parse_legosets_prices(self, legosets: list[Legoset]):
        pass

    @abstractmethod
    async def parse_legoset_images(self, legoset: Legoset):
        pass

    @abstractmethod
    async def parse_legosets_images(self, legosets: list[Legoset]):
        pass