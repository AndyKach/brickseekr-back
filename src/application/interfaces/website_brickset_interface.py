from abc import abstractmethod, ABC
from application.interfaces.website_interface import WebsiteInterface
from application.repositories.legosets_repository import LegosetsRepository
from domain.legoset import Legoset


class WebsiteBrickSetInterface(ABC):
    @abstractmethod
    async def parse_legoset(self, legoset_id: str):
        pass

    @abstractmethod
    async def parse_legosets(self, legosets_repository: LegosetsRepository):
        pass