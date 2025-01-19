from abc import ABC, abstractmethod

from domain.legoset import LegoSet


class LegoSetsRepository(ABC):
    @abstractmethod
    async def get_set(self, set_id: str) -> LegoSet:
        pass

    @abstractmethod
    async def get_all(self) -> [LegoSet]:
        pass

    @abstractmethod
    async def update_url_name(self, lego_set_id: str, url_name: str) -> None:
        pass





