import requests
import asyncio

from bs4 import BeautifulSoup
from lxml import etree
from icecream import ic

from application.interfaces.parser_interface import ParserInterface
from infrastructure.config.logs_config import log_decorator
from infrastructure.config.selenium_config import get_selenium_driver
from infrastructure.db.base import session_factory


class LegoParserInterface(ParserInterface):
    def __init__(self):
        self.driver = None
        self.waiting_time = 2
        self.url = 'https://www.lego.com/de-de/product/'
        self.response = None

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_item(self, item_id: str):
        result = None
        try:
            self.response = requests.get(self.url + item_id)

            result = await self.get_item_info()
            ic(result)

        except Exception as e:
            pass
            print("Error when parsing: ", e)

        # finally:
        #     self.driver.close()
        return result


    async def get_item_info(self):
        # response = requests.get(self.url)
        # soup = BeautifulSoup(self.response.content, 'html.parser')
        soup = BeautifulSoup(self.response.content, 'lxml')
        # ic(soup)
        price_element = soup.find('span',
                                  class_='ds-heading-lg ProductPrice_priceText__ndJDK',
                                  attrs={'data-test': 'product-price'})
        # ic(price_element.get_text(strip=True))
        return price_element.get_text(strip=True).replace('\xa0', ' ')

if __name__ == '__main__':
    lego_parser = LegoParserInterface()
    asyncio.run(lego_parser.parse_item(item_id='60431'))


""
