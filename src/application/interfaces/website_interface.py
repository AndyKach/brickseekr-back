from abc import ABC, abstractmethod
import time

from domain.legoset import Legoset


class WebsiteInterface(ABC):
    def __init__(self):
        self.headers = None

    @abstractmethod
    async def parse_legosets_price(self, legoset: Legoset) -> dict:
        pass

    @abstractmethod
    async def parse_legosets_prices(self, legosets: list[Legoset]):
        pass

    async def fetch_page(self, session, url):
        async with session.get(url, headers=self.headers) as response:
            return await response.text()
