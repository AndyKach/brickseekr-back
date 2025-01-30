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
from application.interfaces.website_data_source_interface import WebsiteDataSourceInterface
from application.interfaces.website_interface import WebsiteInterface
from application.repositories.legosets_repository import LegoSetsRepository
from domain.legoset import LegoSet
from domain.strings_tool_kit import StringsToolKit
from infrastructure.config.logs_config import log_decorator, system_logger
from infrastructure.config.selenium_config import get_selenium_driver
from infrastructure.db.base import session_factory


class WebsiteLegoInterface(WebsiteDataSourceInterface, StringsToolKit):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.waiting_time = 2
        self.url = 'https://www.lego.com/cs-cz/product'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'de-DE,de;q=0.9',
        }
        self.response = None

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legosets_price(self, legoset: LegoSet):
        url = f"{self.url}/{legoset.lego_set_id}"
        async with aiohttp.ClientSession() as session:
            return await self.__get_item_info_bs4(
                session=session, url=url, item_id=legoset.legoset_id
            )

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legosets_prices(self, legosets: list[LegoSet]):
        async with aiohttp.ClientSession() as session:
            rate_limiter = AsyncLimiter(60, 60)
            try:
                async with rate_limiter:
                    tasks = [
                        self.__get_item_info_bs4(
                            session,
                            url=f"{self.url}/{legoset.lego_set_id}",
                            item_id=legoset.lego_set_id
                        ) for legoset in legosets
                    ]
                    # Параллельное выполнение всех задач
                    results = await asyncio.gather(*tasks)
                    return results

            except TooManyRedirects as e:
                print(e)

            return None

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legoset(self, legosets_repository: LegoSetsRepository):
        pass
        # driver = await get_selenium_driver()
        # driver.get(self.url + "/75355")


    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legosets(self, legosets_repository: LegoSetsRepository):
        driver = await get_selenium_driver()
        driver.get(self.url+"/75355")



    async def __get_item_info_bs4(self, session, url: str, item_id: str):
        last_datetime = datetime.now()
        try:
            page = await self.fetch_page(session=session, url=url)
            # with open('test1.txt', 'w') as f:
            #     f.write(str(page))

            # ic(page)
            if page:
                system_logger.info('-------------------------------------')
                system_logger.info('Get page: ' + str(datetime.now() - last_datetime))

                soup = BeautifulSoup(page, 'lxml')
                # with open('test2.txt', 'w') as f:
                #     f.write(str(page))
                # ic(soup)
                legoset_price = soup.find('span',
                                          class_='ds-heading-lg ProductPrice_priceText__ndJDK',
                                          attrs={'data-test': 'product-price'})

                legoset_price_sale = soup.find('span',
                                          class_='ProductPrice_salePrice__L9pb9 ds-heading-lg ProductPrice_priceText__ndJDK',
                                          attrs={'data-test': 'product-price-sale'})

                legoset_minifigures_count = soup.find('span',
                                                  class_='Text__BaseText-sc-13i1y3k-0 gbjGsS ProductAttributesstyles__Value-sc-1sfk910-6 CPPEL',
                                                  attrs={'data-test': 'minifigures-value'})

                legoset_pieces_count = soup.find('span',
                                                 class_='',
                                                 attrs={'data-test': ''})

                legoset_min_age = soup.find('span',
                                                 class_='',
                                                 attrs={'data-test': ''})

                legoset_dimensions = soup.find('span',
                                                 class_='',
                                                 attrs={'data-test': ''})

                legoset_description = soup.find('span',)

                for price_element in [legoset_price, legoset_price_sale]:
                    if price_element:
                        price = price_element.get_text(strip=True)
                        system_logger.info(f'Lego set {item_id} exists, price: {price}')
                        return {"lego_set_id": item_id,
                                "price": price.replace('\xa0', ' ')}

                    else:
                        system_logger.info(f'Lego set {item_id} not found')
        except Exception as e:
            print(f"Error: {e}")


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
