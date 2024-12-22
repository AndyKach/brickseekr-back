from abc import ABC, abstractmethod

class WebsiteController(ABC):
    @abstractmethod
    async def parse_lego_sets_prices(self):
        pass

    @abstractmethod
    async def parse_lego_sets_price(self, lego_set_id: str):
        pass

