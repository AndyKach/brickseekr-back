from abc import ABC, abstractmethod

from domain.legosets_prices import LegoSetsPrices


class LegoSetsPricesRepository(ABC):
    @abstractmethod
    async def save_price(self, lego_set_id: str, website_id: str, price: str) -> None:
        pass

    @abstractmethod
    async def get_item_all_prices(self, lego_set_id: str) -> [str]:
        pass

    @abstractmethod
    async def get_item_price(self, lego_set_id: str, website_id: str) -> str:
        pass

    @abstractmethod
    async def get_item(self, lego_set_id: str) -> LegoSetsPrices:
        pass

    @abstractmethod
    async def get_all_items(self):
        pass


    @abstractmethod
    async def add_item(self, lego_sets_prices: LegoSetsPrices):
        pass


