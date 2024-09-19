from abc import ABC, abstractmethod


class BrickLinkGateway(ABC):
    @abstractmethod
    async def get_item(self, item_type: str, item_id: str):
        pass

    @abstractmethod
    async def get_categories_list(self):
        pass

    @abstractmethod
    async def get_category(self, category_id: str):
        pass


