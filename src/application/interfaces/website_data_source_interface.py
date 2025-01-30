from abc import ABC, abstractmethod

from application.interfaces.website_interface import WebsiteInterface
from application.repositories.legosets_repository import LegoSetsRepository


class WebsiteDataSourceInterface(ABC, WebsiteInterface):
    @abstractmethod
    async def parse_all_legosets(self, legosets_repository: LegoSetsRepository):
        pass

    @abstractmethod
    async def parse_legoset(self, legoset_id: str):
        pass