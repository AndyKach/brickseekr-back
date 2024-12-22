import time
import logging

from application.interfaces.website_interface import WebsiteInterface
from infrastructure.config.logs_config import log_decorator
from infrastructure.config.selenium_config import get_selenium_driver

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

system_logger = logging.getLogger('system_logger')

class WebsiteMuseumOfBricksInterface(WebsiteInterface):

    def __init__(self):
        self.driver = None
        self.waiting_time = 2
        self.url = 'https://eshop.museumofbricks.cz'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'de-DE,de;q=0.9',
        }
        self.response = None

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_lego_sets_url(self, lego_set_id: int | str = "75257"):
        result = {}
        try:
            self.driver = await get_selenium_driver()
            self.driver.get(self.url)
            await self.close_cookies()
            result = await self.open_website(lego_set_id=lego_set_id)

        except Exception as e:
            pass
            print(e)

        finally:
            self.driver.close()

        return result

    @log_decorator(print_args=False, print_kwargs=False)
    async def open_website(self, lego_set_id: int | str):
        system_logger.info("Start searching for lego sets")
        search_element = self.driver.find_element(By.XPATH, "/html/body/div[3]/header/div/div[1]/div[2]/form/fieldset/input[2]")
        search_element.send_keys(str(lego_set_id))

        search_button = self.driver.find_element(By.XPATH, "/html/body/div[3]/header/div/div[1]/div[2]/form/fieldset/button")
        search_button.click()

        time.sleep(5)
        lego_set_button = self.driver.find_element(By.XPATH, "/html/body/div[3]/div[4]/div/main/div[2]/div/div/div/div/div[1]/a/span")
        lego_set_button.click()

        lego_set_url = self.driver.current_url
        system_logger.info(f"Curent url: {lego_set_url}")

        return lego_set_url[lego_set_url.find(lego_set_id)+6:-1]

    async def close_cookies(self):
        try:
            cookies_button = self.driver.find_element(
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