from abc import ABC, abstractmethod

class WebsiteController(ABC):
    @abstractmethod
    async def parse_legosets_prices(self):
        pass

    @abstractmethod
    async def parse_legosets_price(self, lego_set_id: str):
        pass

