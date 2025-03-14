from datetime import datetime

import requests
import asyncio
import aiohttp
from aiolimiter import AsyncLimiter
from aiohttp.client_exceptions import TooManyRedirects
from bs4 import BeautifulSoup
from icecream import ic
from pygments.lexer import words
from lxml import etree

from application.interfaces.parser_interface import ParserInterface
from application.interfaces.website_interface import WebsiteInterface
from domain.legoset import LegoSet
from domain.strings_tool_kit import StringsToolKit
from infrastructure.config.logs_config import log_decorator, system_logger
from infrastructure.config.selenium_config import get_selenium_driver
from infrastructure.db.base import session_factory


class WebsiteCapiCapInterface(WebsiteInterface, StringsToolKit):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.waiting_time = 2
        self.url = "https://www.capi-cap.cz"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'de-DE,de;q=0.9',
        }
        self.response = None

    async def format_lego_set_url(self, legoset: LegoSet):
        legoset_theme = legoset.extendedData.get('cz_category_name')
        if legoset_theme == "None":
            legoset_theme = legoset.theme.lower().replace(' ', '-')
        legoset_url_name = legoset.extendedData.get('cz_url_name')
        if legoset_url_name == "None":
            legoset_url_name = legoset.name.lower().replace(' ', '-').replace('.', '-').replace(':', '-').replace("'", "-")

        yield f"{self.url}/lego-{legoset_theme}-{legoset.id}-{legoset_url_name}"
        yield f"{self.url}/lego-{legoset_theme}--{legoset.id}-{legoset_url_name}"
        yield f"{self.url}/lego---{legoset_theme}-{legoset.id}-{legoset_url_name}"
        yield f"{self.url}/lego---{legoset_theme}--{legoset.id}-{legoset_url_name}"
        yield f"{self.url}/lego-{legoset_theme}-{legoset_url_name}"
        yield f"{self.url}/lego-{legoset_theme}--{legoset_url_name}"

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legosets_price(self, legoset: LegoSet):
        async with aiohttp.ClientSession() as session:
            return await self.__get_lego_sets_price(session=session, legoset=legoset)

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legosets_prices(self, legosets: list[LegoSet]):
        async with aiohttp.ClientSession() as session:
            rate_limiter = AsyncLimiter(60, 60)
            try:
                async with rate_limiter:
                    tasks = [
                        self.__get_lego_sets_price(
                            session=session,
                            legoset=legoset
                        ) for legoset in legosets
                    ]
                    # Параллельное выполнение всех задач
                    results = await asyncio.gather(*tasks)
                    return results

            except TooManyRedirects as e:
                print(e)

            return None


    @log_decorator(print_args=False, print_kwargs=False)
    async def __get_lego_sets_price(self, session, legoset: LegoSet):
        start_time = datetime.now()
        urls = self.format_lego_set_url(legoset=legoset)

        try:
            async for url in urls:
                page = await self.fetch_page(session=session, url=url)

                if page:
                    system_logger.info('-------------------------------------')
                    system_logger.info('Get page: ' + str(datetime.now() - start_time))
                    system_logger.info(f'URL: {url}')

                    soup = BeautifulSoup(page, 'lxml')
                    price_element = soup.find(
                        'strong',
                        class_="price sub-left-position",
                        attrs={'data-testid': "productCardPrice"})

                    if price_element:
                        price = price_element.get_text(strip=True)
                        system_logger.info(f'Legoset {url[url.rfind("/") + 1:]} exists, price: {price}')
                        return {"legoset_id": legoset.id,
                                "price": price.replace('\xa0', ' ')}
                    else:
                        system_logger.info(f'Legoset price not found')
        except Exception as e:
            system_logger.error(e)

    async def fetch_page(self, session, url, limiter_max_rate: int = 60, limiter_time_period: int = 60):
        async with session.get(url, headers=self.headers) as response:
            return await response.text()
