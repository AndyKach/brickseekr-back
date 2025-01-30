from abc import ABC, abstractmethod

class WebsiteDataSourceInterface(ABC):
    @abstractmethod
    async def parse_all_legosets(self):
        pass

    @abstractmethod
    async def parse_legoset(self, legoset_id: str):
        pass