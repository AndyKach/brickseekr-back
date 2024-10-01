from abc import ABC, abstractmethod


class WebsiteInterface(ABC):
    @abstractmethod
    async def parse_item(self, set_id: str):
        pass

    @abstractmethod
    async def parse_items(self, item_ids: list):
        pass
