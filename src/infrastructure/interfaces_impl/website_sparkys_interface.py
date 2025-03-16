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
from domain.legoset import Legoset
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



    @log_decorator()
    async def parse_legosets_price(self, legoset: Legoset) -> dict | None:
        """
         Функция создает новую сессию в браузере и передает ее в парсер

         После чего возвращает полученную новую цену если она есть

         :return: {"legoset_id": str, "price": str} or None
         """
        async with aiohttp.ClientSession() as session:
            return await self.__get_legosets_price(session=session, legoset=legoset)

    @log_decorator()
    async def parse_legosets_prices(self, legosets: list[Legoset]) -> list[dict] | None:
        """
        Функция создает новую сессию в браузере и передает ее в парсер с дополнительным ограничением в 60 штук,
        чтобы сайт не заподозрил скрипт в DDOS

        После чего возвращает полученные новые цены если они есть в формате списка

        :return: list[{"legoset_id": str, "price": str}, {"legoset_id": str, "price": str}] or None
        """
        async with aiohttp.ClientSession() as session:
            rate_limiter = AsyncLimiter(60, 60)
            try:
                async with rate_limiter:
                    tasks = [
                        self.__get_legosets_price(session=session, legoset=legoset) for legoset in legosets
                    ]
                    results = await asyncio.gather(*tasks)
                    return results

            except TooManyRedirects as e:
                system_logger.error(e)

    async def __get_legosets_price(self, session, legoset: Legoset) -> dict | None:
        """
        Функция запрашивает у сессии html код определенной страницы, после чего ищет на ней цену,
        сохраняет ее в словарь и возвращает

        :return: {'lego_set_id': str, 'price': str} or None
        """
        start_time = datetime.now()

        urls = self.__format_legoset_url(legoset=legoset)

        try:
            async for url in urls:
                page = await self.fetch_page(session=session, url=url)

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
                        system_logger.info(f'Legoset {legoset.id} exists, price: {price}')
                        return {
                            "legoset_id": legoset.id,
                            "price": price.replace('\xa0', ' ')
                        }
            system_logger.info(f'Legoset {legoset.id} price not found')
        except Exception as e:
            system_logger.error(e)

    async def __format_legoset_url(self, legoset: Legoset):
        """
        Функция возвращает всевозможные комбинации темы, ID и имени наборов для сайта

        yield нужен для того, чтобы при каждом новом запросе к функции возвращалось следующее значение
        """
        legoset_theme = legoset.extendedData.get('cz_category_name')
        if legoset_theme == "None":
            legoset_theme = legoset.theme.lower().replace(' ', '-')
        legoset_url_name = legoset.extendedData.get('cz_url_name')
        if legoset_url_name == "None":
            legoset_url_name = legoset.name.lower().replace(' ', '-').replace('.', '-').replace(':', '-').replace("'", "-")

        yield f"{self.url}/lego-{legoset_theme}-{legoset.id}-{legoset_url_name}"
        yield f"{self.url}/lego-{legoset_theme}-{legoset_url_name}"
        yield f"{self.url}/lego-{legoset_theme}-{legoset.id}"
        yield f"{self.url}/lego-{legoset_theme}-{legoset_url_name}"