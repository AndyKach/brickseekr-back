from abc import ABC, abstractmethod

class ParserInterface(ABC):
    @abstractmethod
    async def parse_item(self,item_type: str, item_id: str):
        pass
