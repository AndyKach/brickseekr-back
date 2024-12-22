from abc import ABC, abstractmethod

from domain.lego_sets_prices import LegoSetsPrices


class LegoSetsPricesRepository(ABC):
    @abstractmethod
    async def save_price(self, item_id: str, website_id: str, price: str) -> None:
        pass

    @abstractmethod
    async def get_item_all_prices(self, item_id: str) -> [str]:
        pass

    @abstractmethod
    async def get_item_price(self, item_id: str, website_id: str) -> str:
        pass

    @abstractmethod
    async def get_item(self, item_id: str) -> LegoSetsPrices:
        pass

    @abstractmethod
    async def get_all_items(self):
        pass


    @abstractmethod
    async def add_item(self, lego_sets_prices: LegoSetsPrices):
        pass


