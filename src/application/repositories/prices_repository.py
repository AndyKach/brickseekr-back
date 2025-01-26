from abc import ABC, abstractmethod

from domain.legosets_price import LegoSetsPrice
from domain.legosets_prices import LegoSetsPrices


class LegoSetsPricesRepository(ABC):
    @abstractmethod
    async def save_price(self, legoset_id: str, website_id: int, price: str) -> None:
        pass

    @abstractmethod
    async def get_item_all_prices(self, legoset_id: str) -> LegoSetsPrices:
        pass

    @abstractmethod
    async def get_item_price(self, legoset_id: str, website_id: int) -> LegoSetsPrice:
        pass

    @abstractmethod
    async def get_item(self, lego_set_id: str) -> LegoSetsPrices:
        pass

    @abstractmethod
    async def get_all_items(self):
        pass


    @abstractmethod
    async def add_item(self, legosets_prices: LegoSetsPrices):
        pass


