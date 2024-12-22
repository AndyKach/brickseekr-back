import time
import logging
from datetime import datetime
from application.interfaces.website_interface import WebsiteInterface
from domain.lego_set import LegoSet
from infrastructure.config.logs_config import log_decorator
from infrastructure.config.selenium_config import get_selenium_driver
import asyncio
import aiohttp
from aiolimiter import AsyncLimiter
from aiohttp.client_exceptions import TooManyRedirects

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

system_logger = logging.getLogger('system_logger')

class WebsiteMuseumOfBricksInterface(WebsiteInterface):

    def __init__(self):
        self.driver = None
        self.waiting_time = 0
        self.url = 'https://eshop.museumofbricks.cz'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'de-DE,de;q=0.9',
        }
        self.response = None


    async def parse_lego_sets_urls_async(self, lego_sets):
        drivers = [await get_selenium_driver() for _ in range(4)]
        tasks = [
            self.parse_lego_sets_urls(driver=drivers[0], lego_sets=lego_sets[:5]),
            self.parse_lego_sets_urls(driver=drivers[1], lego_sets=lego_sets[5:10]),
            self.parse_lego_sets_urls(driver=drivers[2], lego_sets=lego_sets[10:15]),
            self.parse_lego_sets_urls(driver=drivers[3], lego_sets=lego_sets[15:20])
        ]
        # tasks += [self.parse_lego_sets_urls(driver=drivers[2], lego_set_id=lego_set.lego_set_id) for lego_set in lego_sets[10:15]]
        # tasks += [self.parse_lego_sets_urls(driver=drivers[3], lego_set_id=lego_set.lego_set_id) for lego_set in lego_sets[15:20]]
        # print(tasks)
        return await asyncio.gather(*tasks)

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_lego_sets_urls(self, lego_sets: list[LegoSet]):
        result = []
        start_time_all = datetime.now()

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
    async def parse_lego_sets_url(self, lego_set_id: int | str = "75257"):
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
    async def open_website(self, lego_set_id: int | str, driver):
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




    async def close_cookies(self, driver):
        try:
            cookies_button = driver.find_element(
                By.CSS_SELECTOR,
                'button.siteCookies__button.js-cookiesConsentSubmit[data-testid="buttonCookiesAccept"]'
            )
            cookies_button.click()
        except Exception as e:
            print(e)



    async def parse_item(self, item_id: str):
        pass

    async def parse_items(self, item_ids: list):
        pass