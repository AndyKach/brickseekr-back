from abc import ABC, abstractmethod

class GoogleInterface(ABC):
    @abstractmethod
    async def get_legosets_rating(self, legoset_id: str):
        pass