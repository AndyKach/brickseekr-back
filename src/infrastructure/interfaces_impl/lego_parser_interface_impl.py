from datetime import datetime

import requests
import asyncio
import aiohttp

from bs4 import BeautifulSoup
from icecream import ic

from application.interfaces.parser_interface import ParserInterface
from infrastructure.config.logs_config import log_decorator, system_logger
from infrastructure.config.selenium_config import get_selenium_driver
from infrastructure.db.base import session_factory


class LegoParserInterface(ParserInterface):
    def __init__(self):
        self.driver = None
        self.waiting_time = 2
        self.url = 'https://www.lego.com/de-de/product/'
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
            result = await self.get_item_info(session=session, url=url)
        # try:

        # last_datetime = datetime.now()
        # system_logger.info('get page request')
        #
        # async with aiohttp.ClientSession() as session:
        #     tasks = [self.fetch_page(session=session, url=self.url + item_id)]
        #     page = await asyncio.gather(*tasks)

        # self.response = requests.get(self.url + item_id, headers=self.headers)

        # system_logger.info(datetime.now() - last_datetime)
        # last_datetime = datetime.now()
        #
        # result = await self.get_item_info(page=page)
        # system_logger.info(datetime.now() - last_datetime)
        # last_datetime = datetime.now()

        # system_logger.info(result)


        # except Exception as e:
        #     pass
        #     print("Error when parsing: ", e)

        # finally:
        #     self.driver.close()
        return result

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_items(self, item_ids: list):
        async with aiohttp.ClientSession() as session:
            tasks = [await self.get_item_info(session, url=self.url + item_id) for item_id in item_ids]
            # Параллельное выполнение всех задач
            results = await asyncio.gather(*tasks)
            return results


    async def get_item_info(self, session, url: str):

        last_datetime = datetime.now()
        page = await self.fetch_page(session=session, url=url)
        system_logger.info('Get page: ' + str(datetime.now() - last_datetime))

        soup = BeautifulSoup(page, 'lxml')

        price_element = soup.find('span',
                                  class_='ds-heading-lg ProductPrice_priceText__ndJDK',
                                  attrs={'data-test': 'product-price'})

        if price_element:
            price = price_element.get_text(strip=True)
            system_logger.info(f'Lego set {url[url.rfind("/")+1:]} exists, price: {price}')
            system_logger.info(f"Price found: {price}")
            return price_element.get_text(strip=True).replace('\xa0', ' ')

        else:
            system_logger.info(f'Lego set {url[url.rfind("/")+1:]} not found')
            system_logger.info("Price element not found")
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

    async def fetch_page(self, session, url):
        async with session.get(url, headers=self.headers) as response:
            return await response.text()


if __name__ == '__main__':
    lego_parser = LegoParserInterface()
    # asyncio.run(lego_parser.parse_item(item_id='60431'))
    asyncio.run(lego_parser.get_all_info_about_item(item_id='60431'))
    asyncio.run(lego_parser.get_all_info_about_item(item_id='61505'))



""
