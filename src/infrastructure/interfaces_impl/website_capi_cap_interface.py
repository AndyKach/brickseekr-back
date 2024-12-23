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
from domain.lego_set import LegoSet
from domain.strings_tool_kit import StringsToolKit
from infrastructure.config.logs_config import log_decorator, system_logger
from infrastructure.config.selenium_config import get_selenium_driver
from infrastructure.db.base import session_factory


class WebsiteCapiCapInterface(WebsiteInterface, StringsToolKit):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.waiting_time = 2
        self.url = 'https://www.capi-cap.cz/lego-{category}-{artikel}-{name}/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'de-DE,de;q=0.9',
        }
        self.response = None

    async def format_lego_set_url(self, lego_set: LegoSet):
        return self.url.format(category=lego_set.category_name, artikel=lego_set.lego_set_id, name=lego_set.url_name)
        # return f"{self.url}/lego-{lego_set.category_name}--{lego_set.lego_set_id}-{lego_set.url_name}"

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


    @log_decorator(print_args=False, print_kwargs=False)
    async def __get_lego_sets_price(self, session, url: str, item_id: str):
        start_time = datetime.now()
        page = await self.fetch_page(session=session, url=url)
        # with open('test1.txt', 'w') as f:
        #     f.write(str(page))

        # ic(page)
        if page:
            system_logger.info('-------------------------------------')
            system_logger.info('Get page: ' + str(datetime.now() - start_time))
            system_logger.info(f'URL: {url}')

            soup = BeautifulSoup(page, 'lxml')
            # print(f"DOM:\n{soup}")
            # set_price = dom.xpath('/html/body/div[4]/div/div[1]/div[2]/div/div/main/div/form/fieldset/table/tbody/tr/td[2]/table[1]/tbody/tr[3]/td[1]/strong')
            price_element = soup.find(
                'strong',
                class_="price sub-left-position",
                attrs={'data-testid': "productCardPrice"})

            if price_element:
                price = price_element.get_text(strip=True)
                system_logger.info(f'Lego set {url[url.rfind("/") + 1:]} exists, price: {price}')
                return {"lego_set_id": item_id,
                        "price": price.replace('\xa0', ' ')}
            else:
                system_logger.info(f'Lego set price not found')

    async def fetch_page(self, session, url, limiter_max_rate: int = 60, limiter_time_period: int = 60):
        async with session.get(url, headers=self.headers) as response:
            return await response.text()
