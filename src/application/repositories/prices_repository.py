from abc import ABC, abstractmethod

from domain.legosets_price import LegosetsPrice
from domain.legosets_prices import LegosetsPrices


class LegosetsPricesRepository(ABC):
    @abstractmethod
    async def save_price(self, legoset_id: str, website_id: str, price: str) -> None:
        pass

    @abstractmethod
    async def get_item_all_prices(self, legoset_id: str) -> LegosetsPrices:
        pass

    @abstractmethod
    async def get_item_price(self, legoset_id: str, website_id: str) -> LegosetsPrice:
        pass

    @abstractmethod
    async def get_item(self, legoset_id: str) -> LegosetsPrices:
        pass

    @abstractmethod
    async def get_all_items(self):
        pass


    @abstractmethod
    async def add_items(self, legosets_prices: LegosetsPrices):
        pass

    @abstractmethod
    async def add_item(self, legosets_price: LegosetsPrice):
        pass

    @abstractmethod
    async def delete_price(self, legoset_id: str, website_id: str):
        pass


