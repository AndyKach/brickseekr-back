from abc import ABC, abstractmethod


class PriceRepository(ABC):
    @abstractmethod
    async def save_price(self, item_id: str, web_site_id: str, price: str) -> None:
        pass

    @abstractmethod
    async def get_item_all_prices(self, item_id: str) -> [str]:
        pass

    @abstractmethod
    async def get_item_price(self, item_id: str, web_site_id: str) -> str:
        pass