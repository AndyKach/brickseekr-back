from abc import ABC, abstractmethod

from domain.legoset import Legoset


class LegoSetsRepository(ABC):
    @abstractmethod
    async def get_set(self, set_id: str) -> Legoset:
        pass

    @abstractmethod
    async def get_all(self) -> list[Legoset]:
        pass

    @abstractmethod
    async def get_top_rating(self, legosets_count: int):
        pass

    @abstractmethod
    async def set_set(self, legoset: Legoset) -> None:
        pass

    @abstractmethod
    async def update_set(self, legoset: Legoset) -> None:
        pass

    @abstractmethod
    async def update_rating(self, legoset_id: str, rating: float) -> None:
        pass

    @abstractmethod
    async def update_google_rating(self, legoset_id: str, google_rating: float) -> None:
        pass

    @abstractmethod
    async def update_extended_data(self, legoset_id: str, extended_data: dict) -> None:
        """
        extended_data: {"cz_url_name": str, "cz_category_name": str}
        """
        pass

    @abstractmethod
    async def update_images(self, legoset_id: str, images: dict) -> None:
        pass


