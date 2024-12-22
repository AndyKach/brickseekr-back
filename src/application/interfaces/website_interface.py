from abc import ABC, abstractmethod
import time

from domain.lego_set import LegoSet


class WebsiteInterface(ABC):
    def __init__(self):
        self.headers = None

    @abstractmethod
    async def parse_lego_sets_price(self, lego_set: LegoSet) -> dict:
        pass

    @abstractmethod
    async def parse_lego_sets_prices(self, lego_sets: list[LegoSet]):
        pass

    async def fetch_page(self, session, url, limiter_max_rate: int = 60, limiter_time_period: int = 60):
        async with session.get(url, headers=self.headers) as response:
            return await response.text()
