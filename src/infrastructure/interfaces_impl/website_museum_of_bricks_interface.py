import time
import logging
from datetime import datetime
from application.interfaces.website_interface import WebsiteInterface
from domain.legoset import LegoSet
from infrastructure.config.logs_config import log_decorator
from infrastructure.config.selenium_config import get_selenium_driver
import asyncio
import aiohttp
from aiolimiter import AsyncLimiter
from aiohttp.client_exceptions import TooManyRedirects
from bs4 import BeautifulSoup
from icecream import ic


from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

system_logger = logging.getLogger('system_logger')

class WebsiteMuseumOfBricksInterface(WebsiteInterface):

    def __init__(self):
        super().__init__()
        self.driver = None
        self.waiting_time = 0
        self.url = 'https://eshop.museumofbricks.cz'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'de-DE,de;q=0.9',
        }
        self.response = None


    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_lego_sets_urls(self, lego_sets: list[LegoSet]):
        result = []
        start_time_all = datetime.now()
        driver = None
        try:
            driver = await get_selenium_driver()
            driver.get(self.url)
            await self.close_cookies(driver=driver)
            for lego_set in lego_sets:
                start_time = datetime.now()

                result.append(await self.open_website(lego_set_id=lego_set.lego_set_id, driver=driver))

                # system_logger.info(f"Result: {result}")
                system_logger.info(f"One lego set time: {datetime.now() - start_time}")
                system_logger.info('=======================')

        except Exception as e:
            pass
            print(e)

        finally:
            driver.close()

        system_logger.info(f"All parse time: {datetime.now() - start_time_all}")


        return result

    @log_decorator(print_args=False, print_kwargs=True)
    async def parse_lego_sets_url(self, lego_set_id: str):
        result = {}
        start_time = datetime.now()
        driver = None
        try:
            driver = await get_selenium_driver()
            driver.get(self.url)
            await self.close_cookies(driver=driver)
            result = await self.open_website(lego_set_id=lego_set_id, driver=driver)

        except Exception as e:
            pass
            print(e)

        finally:
            driver.close()

        system_logger.info(datetime.now()-start_time)

        return result

    @log_decorator(print_args=False, print_kwargs=False)
    async def open_website(self, lego_set_id: str, driver):
        system_logger.info("Start searching for lego sets")
        search_element = driver.find_element(By.XPATH, "/html/body/div[3]/header/div/div[1]/div[2]/form/fieldset/input[2]")
        search_element.clear()
        search_element.send_keys(str(lego_set_id))

        search_button = driver.find_element(By.XPATH, "/html/body/div[3]/header/div/div[1]/div[2]/form/fieldset/button")
        search_button.click()

        # time.sleep(self.waiting_time)

        try:
            lego_set_button = driver.find_element(By.XPATH, "/html/body/div[3]/div[4]/div/main/div[2]/div/div/div/div/div[1]/a/span")
            lego_set_button.click()
            lego_set_url = driver.current_url
            system_logger.info(f"\nLego set: {lego_set_id}\nCurent url: {lego_set_url}\n===============")
            return {
                "id": lego_set_id,
                "url": lego_set_url[lego_set_url.find(lego_set_id) + 6:-1]
            }
        except:
            system_logger.info(f"\nLego set: {lego_set_id}\nSet not found\n===============")
            return {
                "id": lego_set_id,
                "url": "no_url"
            }

    @log_decorator(print_args=False, print_kwargs=False)
    async def close_cookies(self, driver):
        try:
            cookies_button = driver.find_element(
                By.CSS_SELECTOR,
                'button.siteCookies__button.js-cookiesConsentSubmit[data-testid="buttonCookiesAccept"]'
            )
            cookies_button.click()
        except Exception as e:
            print(e)

    async def format_lego_set_url(self, lego_set: LegoSet):
        if lego_set.category_name == 'disney':
            yield f"{self.url}/lego---{lego_set.category_name}-{lego_set.lego_set_id}-{lego_set.url_name}"
            yield f"{self.url}/lego---{lego_set.category_name}-princess-{lego_set.lego_set_id}-{lego_set.url_name}"
        yield f"{self.url}/lego-{lego_set.category_name}-{lego_set.lego_set_id}-{lego_set.url_name}"
        yield f"{self.url}/lego-{lego_set.category_name}--{lego_set.lego_set_id}-{lego_set.url_name}"
        yield f"{self.url}/lego-{lego_set.category_name}-{lego_set.lego_set_id}-{lego_set.url_name}"
        yield f"{self.url}/lego--{lego_set.category_name}--{lego_set.lego_set_id}-{lego_set.url_name}"
        yield f"{self.url}/lego-{lego_set.lego_set_id}-{lego_set.url_name}"

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
                            lego_set=lego_set,
                        ) for lego_set in legosets
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

            if page:
                system_logger.info('-------------------------------------')
                system_logger.info('Get page: ' + str(datetime.now() - start_time))

                soup = BeautifulSoup(page, 'lxml')

                price_element = soup.find('span', class_="price-final-holder")

                if price_element:
                    price = price_element.get_text(strip=True)
                    system_logger.info(f'Lego set {url[url.rfind("/") + 1:]} exists, price: {price}')
                    return {
                        "lego_set_id": lego_set.lego_set_id,
                        "price": price.replace('\xa0', ' ')
                    }
                else:
                    system_logger.info(f'Lego set price not found')