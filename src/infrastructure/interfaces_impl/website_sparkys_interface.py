from datetime import datetime

import requests
import asyncio
import aiohttp
from aiolimiter import AsyncLimiter
from aiohttp.client_exceptions import TooManyRedirects
from bs4 import BeautifulSoup
from icecream import ic
from pygments.lexer import words

from application.interfaces.parser_interface import ParserInterface
from application.interfaces.website_interface import WebsiteInterface
from domain.lego_set import LegoSet
from domain.strings_tool_kit import StringsToolKit
from infrastructure.config.logs_config import log_decorator, system_logger


class WebsiteSparkysInterface(WebsiteInterface, StringsToolKit):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.waiting_time = 2
        self.url = 'https://www.sparkys.cz'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'de-DE,de;q=0.9',
        }
        self.response = None


    async def format_lego_set_url(self, lego_set: LegoSet):
        return f"{self.url}/lego-{lego_set.category_name}-{lego_set.lego_set_id}-{lego_set.url_name}"

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_lego_sets_price(self, lego_set: LegoSet):
        url = await self.format_lego_set_url(lego_set=lego_set)
        async with aiohttp.ClientSession() as session:
            return await self.__get_lego_sets_price(session=session, url=url, item_id=lego_set.lego_set_id)

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_lego_sets_prices(self, lego_sets: list[LegoSet]):
        async with aiohttp.ClientSession() as session:
            rate_limiter = AsyncLimiter(60, 60)
            try:
                async with rate_limiter:
                    tasks = [
                        self.__get_lego_sets_price(
                            session,
                            url=await self.format_lego_set_url(lego_set=lego_set),
                            item_id=lego_set.lego_set_id
                        ) for lego_set in lego_sets
                    ]
                    # Параллельное выполнение всех задач
                    results = await asyncio.gather(*tasks)
                    return results

            except TooManyRedirects as e:
                print(e)

            return None


    async def __get_lego_sets_price(self, session, url: str, item_id: str):
        start_time = datetime.now()
        page = await self.fetch_page(session=session, url=url)

        # print(url)

        if page:
            system_logger.info('-------------------------------------')
            system_logger.info('Get page: ' + str(datetime.now() - start_time))
            system_logger.info(f'URL: {url}')

            soup = BeautifulSoup(page, 'lxml')

            price_element = soup.find('div', class_="Product-priceFinal")
            # print(f"price_element: {price_element}")
            if price_element:
                price = price_element.get_text(strip=True)
                price = price.replace('&nbsp;', ' ')
                system_logger.info(f'Lego set {url[url.rfind("/") + 1:]} exists, price: {price}')
                return {
                    "lego_set_id": item_id,
                    "price": price.replace('\xa0', ' ')
                }
            else:
                system_logger.info(f'Lego set price not found')