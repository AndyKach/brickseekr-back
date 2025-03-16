from application.interfaces.website_interface import WebsiteInterface
from abc import ABC, abstractmethod

from domain.legoset import Legoset


class WebsiteMuseumOfBricksInterface(WebsiteInterface):
    @abstractmethod
    async def parse_legosets_price(self, legoset: Legoset) -> dict:
        pass

    @abstractmethod
    async def parse_legosets_prices(self, legosets: list[Legoset]):
        pass

    @abstractmethod
    async def parse_legosets_url(self, legoset_id: str) -> dict | None:
        pass

    @abstractmethod
    async def parse_legosets_urls(self, legosets: list[Legoset]) -> list[dict] | None:
        pass