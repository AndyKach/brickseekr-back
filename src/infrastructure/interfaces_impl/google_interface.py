import json
import logging
import time
from datetime import datetime
from random import random
import re
import aiohttp
from bs4 import BeautifulSoup
from icecream import ic
from selenium.webdriver.common.by import By
from application.interfaces.google_interface import GoogleInterface
from infrastructure.config.selenium_config import get_selenium_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

system_logger = logging.getLogger('system_logger')
class GoogleInterfaceImpl(GoogleInterface):
    def __init__(self):
        self.driver = None

        # self.url = "https://www.google.com/search?q=lego+"
        self.url = 'https://www.lego.com/en-cz'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'de-DE,de;q=0.9',
        }

    async def open_driver(self):
        self.driver = await get_selenium_driver()

    async def close_driver(self):
        self.driver.close()

    async def get_legosets_rating(self, legoset_id: str):
        """
        Эта функция будет позже изменена на корректную с использованием SearchAPI
        """
        url = f"{self.url}/product/{legoset_id}"
        rating = None

        self.driver.get(url)
        time.sleep(3)
        wait = WebDriverWait(self.driver, 10)
        try:
            rating_element = self.driver.find_element(By.CSS_SELECTOR,
                                          "[data-test='product-overview-rating']")

            match = re.search(r"(\d+\.\d+)", rating_element.text)
            if match:
                rating = float(match.group(1))
                if rating:
                    return float(rating)
        except Exception as e:
            system_logger.error(f"Legoset: {legoset_id} by parsing have EXCEPTION: {e}")
