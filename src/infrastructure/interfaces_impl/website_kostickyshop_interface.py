import logging
from datetime import datetime

from bs4 import BeautifulSoup

from application.interfaces.website_interface import WebsiteInterface
from domain.legoset import LegoSet
from infrastructure.config.logs_config import log_decorator
import asyncio
import aiohttp
from aiolimiter import AsyncLimiter
from aiohttp.client_exceptions import TooManyRedirects

system_logger = logging.getLogger('system_logger')

class WebsiteKostickyshopInterface(WebsiteInterface):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.waiting_time = 0
        self.url = 'https://www.kostickyshop.cz'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'de-DE,de;q=0.9',
        }
        self.response = None

    async def format_lego_set_url(self, lego_set: LegoSet):
        yield f"{self.url}/lego-{lego_set.category_name}-{lego_set.lego_set_id}-{lego_set.url_name}"
        yield f"{self.url}/lego-{lego_set.lego_set_id}-{lego_set.url_name}"
        # return f"{self.url}/lego-{lego_set.category_name}--{lego_set.lego_set_id}-{lego_set.url_name}"

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legosets_price(self, lego_set: LegoSet):
        async with aiohttp.ClientSession() as session:
            return await self.__get_lego_sets_price(session=session, lego_set=lego_set)

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legosets_prices(self, lego_sets: list[LegoSet]):
        async with aiohttp.ClientSession() as session:
            rate_limiter = AsyncLimiter(60, 60)
            try:
                async with rate_limiter:
                    tasks = [
                        self.__get_lego_sets_price(
                            session=session,
                            lego_set=lego_set
                        ) for lego_set in lego_sets
                    ]
                    # Параллельное выполнение всех задач
                    results = await asyncio.gather(*tasks)
                    return results

            except TooManyRedirects as e:
                print(e)

            return None

    @log_decorator(print_args=False, print_kwargs=False)
    async def __get_lego_sets_price(self, session: aiohttp.ClientSession, lego_set: LegoSet):
        start_time = datetime.now()
        urls = self.format_lego_set_url(lego_set=lego_set)
        async for url in urls:
            page = await self.fetch_page(session=session, url=url)
            # print(url)
            # print(page)
            if page:
                print('!!!!!!!!!!!!!!!!')
                system_logger.info('-------------------------------------')
                system_logger.info('Get page: ' + str(datetime.now() - start_time))
                system_logger.info(f'URL: {url}')


                soup = BeautifulSoup(page, 'lxml')

                price_element = soup.find('b', class_="product-card-price2")

                if price_element:
                    price = price_element.get_text(strip=True)
                    system_logger.info(f'Lego set {url[url.rfind("/") + 1:]} exists, price: {price}')
                    return {
                        "lego_set_id": lego_set.lego_set_id,
                        "price": price.replace('\xa0', ' ')
                    }
                else:
                    system_logger.info(f'Lego set price not found')

