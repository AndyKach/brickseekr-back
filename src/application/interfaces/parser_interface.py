from abc import ABC, abstractmethod

class ParserInterface(ABC):
    @abstractmethod
    async def parse_item(self, item_id: str):
        pass
