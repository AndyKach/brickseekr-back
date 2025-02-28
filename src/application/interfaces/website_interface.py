from abc import ABC, abstractmethod
import time

from domain.legoset import LegoSet


class WebsiteInterface(ABC):
    def __init__(self):
        self.headers = None

    @abstractmethod
    async def parse_legosets_price(self, legoset: LegoSet) -> dict:
        pass

    @abstractmethod
    async def parse_legosets_prices(self, legosets: list[LegoSet]):
        pass

    async def fetch_page(self, session, url, limiter_max_rate: int = 60, limiter_time_period: int = 60):
        async with session.get(url, headers=self.headers) as response:
            return await response.text()
