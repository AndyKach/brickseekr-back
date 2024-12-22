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
from infrastructure.config.selenium_config import get_selenium_driver
from infrastructure.db.base import session_factory


class WebsiteLegoInterface(WebsiteInterface, StringsToolKit):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.waiting_time = 2
        self.url = 'https://www.lego.com/de-de/product/{artikel}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'de-DE,de;q=0.9',
        }
        self.response = None

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_lego_sets_price(self, lego_set: str):
        result = None
        url = self.url + lego_set
        async with aiohttp.ClientSession() as session:
            result = await self.__get_item_info(session=session, item_id=lego_set)

        return result

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_lego_sets_prices(self, lego_sets: list[LegoSet]):
        async with aiohttp.ClientSession() as session:
            rate_limiter = AsyncLimiter(60, 60)
            try:
                async with rate_limiter:
                    tasks = [
                        self.__get_item_info(
                            session,
                            url=self.url.format(
                                name=self.normalize_string(lego_set.name),
                                artikel=lego_set.lego_set_id
                            ),
                            item_id=lego_set.lego_set_id
                        ) for lego_set in lego_sets
                    ]
                    # Параллельное выполнение всех задач
                    results = await asyncio.gather(*tasks)
                    return results

            except TooManyRedirects as e:
                print(e)

            return None


    async def __get_item_info(self, session, url: str, item_id: str):
        last_datetime = datetime.now()
        page = await self.fetch_page(session=session, url=url)
        with open('test1.txt', 'w') as f:
            f.write(str(page))

        # ic(page)
        if page:
            system_logger.info('-------------------------------------')
            system_logger.info('Get page: ' + str(datetime.now() - last_datetime))

            soup = BeautifulSoup(page, 'lxml')
            # with open('test2.txt', 'w') as f:
            #     f.write(str(page))
            # ic(soup)
            set_price = soup.find('span',
                                      class_='ds-heading-lg ProductPrice_priceText__ndJDK',
                                      attrs={'data-test': 'product-price'})

            set_price_sale = soup.find('span',
                                      class_='ProductPrice_salePrice__L9pb9 ds-heading-lg ProductPrice_priceText__ndJDK',
                                      attrs={'data-test': 'product-price-sale'})

            for price_element in [set_price, set_price_sale]:
                if price_element:
                    price = price_element.get_text(strip=True)
                    system_logger.info(f'Lego set {item_id} exists, price: {price}')
                    return {"lego_set_id": item_id,
                            "price": price.replace('\xa0', ' ')}

                else:
                    system_logger.info(f'Lego set {item_id} not found')



        return None
            # ic(price_element.get_text(strip=True))

    async def get_all_info_about_item(self, item_id: str):
        self.response = requests.get(self.url + item_id)
        soup = BeautifulSoup(self.response.content, 'lxml')
        price_element = soup.find('span',
                                  class_='ds-heading-lg ProductPrice_priceText__ndJDK',
                                  attrs={'data-test': 'product-price'})
        ic(soup)
        ic(price_element)
        if price_element:
            teile = soup.find('div',
                              class_='ProductAttributesstyles__ValueWrapper-sc-1sfk910-5 jNaXJo',
                              attrs={'data-test': "pieces-value"})
            ic(teile)

            element = soup.find('div', {'data-test': 'pieces-value',
                                        'class': 'ProductAttributesstyles__ValueWrapper-sc-1sfk910-5 jNaXJo'})
            ic(element)

    async def fetch_page(self, session, url, limiter_max_rate: int = 60, limiter_time_period: int = 60):
        async with session.get(url, headers=self.headers) as response:
            return await response.text()

        # rate_limiter = AsyncLimiter(limiter_max_rate, limiter_time_period)
        # try:
        #     async with rate_limiter:
        #         async with session.get(url, headers=self.headers) as response:
        #             return await response.text()
        # except TooManyRedirects as e:
        #     print(e)


if __name__ == '__main__':
    lego_parser = WebsiteLegoInterface()
    # asyncio.run(lego_parser.parse_item(item_id='60431'))
    asyncio.run(lego_parser.get_all_info_about_item(item_id='60431'))
    asyncio.run(lego_parser.get_all_info_about_item(item_id='61505'))



""
