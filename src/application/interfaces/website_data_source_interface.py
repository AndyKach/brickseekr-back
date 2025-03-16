from abc import ABC, abstractmethod

from application.interfaces.website_interface import WebsiteInterface
from application.repositories.legosets_repository import LegoSetsRepository
from domain.legoset import Legoset


class WebsiteDataSourceInterface:
    @abstractmethod
    async def parse_legoset(self, legoset_id: str):
        pass

    @abstractmethod
    async def parse_legosets(self):
        pass