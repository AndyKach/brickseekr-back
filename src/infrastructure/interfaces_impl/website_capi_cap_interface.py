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
from infrastructure.config.logs_config import log_decorator, system_logger
from infrastructure.config.selenium_config import get_selenium_driver
from infrastructure.db.base import session_factory


class WebsiteCapiCapInterface(WebsiteInterface):
    def __init__(self):
        self.driver = None
        self.waiting_time = 2
        self.url = 'https://www.capi-cap.cz/lego-star-wars--{name}-/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'de-DE,de;q=0.9',
        }
        self.response = None

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_item(self, item_id: str):
        result = None
        url = self.url + item_id
        async with aiohttp.ClientSession() as session:
            result = await self.__get_item_info(session=session, item_id=item_id)

        return result

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_items(self, item_id: str):
        pass

    @log_decorator(print_args=False, print_kwargs=False)
    async def __get_item_info(self, session, item_url: str):
        last_datetime = datetime.now()
        page = await self.fetch_page(session=session, url=item_url)
        with open('test1.txt', 'w') as f:
            f.write(str(page))

        # ic(page)
        if page:
            system_logger.info('-------------------------------------')
            system_logger.info('Get page: ' + str(datetime.now() - last_datetime))

    async def fetch_page(self, session, url, limiter_max_rate: int = 60, limiter_time_period: int = 60):
        async with session.get(url, headers=self.headers) as response:
            return await response.text()
