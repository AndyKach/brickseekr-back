from abc import ABC, abstractmethod

class ParserInterface(ABC):
    @abstractmethod
    async def parse_item(self, item_id: str):
        pass

    @abstractmethod
    async def parse_items(self, item_ids: list):
        pass