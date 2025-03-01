from abc import ABC, abstractmethod

from application.interfaces.website_interface import WebsiteInterface
from application.repositories.legosets_repository import LegoSetsRepository
from domain.legoset import LegoSet


class WebsiteDataSourceInterface(WebsiteInterface):
    # @abstractmethod
    # async def parse_legosets(self, legosets_repository: LegoSetsRepository):
    #
    #     pass
    #
    # @abstractmethod
    # async def parse_legoset(self, legoset_id: str):
    #     pass

    @abstractmethod
    async def parse_legosets_price(self, legoset_id: str) -> dict:
        pass

    @abstractmethod
    async def parse_legosets_prices(self, legosets: list[LegoSet]):
        pass