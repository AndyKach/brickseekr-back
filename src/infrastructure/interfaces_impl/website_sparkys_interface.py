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
from domain.legoset import LegoSet
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
        yield f"{self.url}/lego-{lego_set.category_name}-{lego_set.lego_set_id}-{lego_set.url_name}"
        yield f"{self.url}/lego-{lego_set.category_name}-{lego_set.url_name}"
        yield f"{self.url}/lego-{lego_set.category_name}-{lego_set.lego_set_id}"
        yield f"{self.url}/lego-{lego_set.lego_set_id}-{lego_set.url_name}"
        yield f"{self.url}/{lego_set.url_name}"

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legosets_price(self, legoset: LegoSet):
        async with aiohttp.ClientSession() as session:
            return await self.__get_lego_sets_price(session=session, lego_set=legoset)

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legosets_prices(self, legosets: list[LegoSet]):
        async with aiohttp.ClientSession() as session:
            rate_limiter = AsyncLimiter(60, 60)
            try:
                async with rate_limiter:
                    tasks = [
                        self.__get_lego_sets_price(
                            session=session,
                            lego_set=lego_set
                        ) for lego_set in legosets
                    ]
                    # Параллельное выполнение всех задач
                    results = await asyncio.gather(*tasks)
                    return results

            except TooManyRedirects as e:
                print(e)

            return None

    async def __get_lego_sets_price(self, session, lego_set: LegoSet):
        """
        :param session: Async session
        :param lego_set: LegoSet object
        :return: {'lego_set_id': str, 'price': str} or None
        """
        start_time = datetime.now()

        urls = self.format_lego_set_url(lego_set=lego_set)

        async for url in urls:
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
                    price = price.replace(' ', '')
                    system_logger.info(f'Lego set {lego_set.lego_set_id} exists, price: {price}')
                    return {
                        "lego_set_id": lego_set.lego_set_id,
                        "price": price.replace('\xa0', ' ')
                    }

        system_logger.info(f'Lego set {lego_set.lego_set_id} price not found')
        return None
