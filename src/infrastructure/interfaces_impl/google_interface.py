import logging
from application.interfaces.google_interface import GoogleInterface
from serpapi import Client
import os

from infrastructure.config.logs_config import log_decorator

system_logger = logging.getLogger('system_logger')
class GoogleInterfaceImpl(GoogleInterface):
    def __init__(self):
        self.driver = None

        self.url = "https://www.google.com/search?q=lego+"
        # self.url = 'https://www.lego.com/en-cz'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'de-DE,de;q=0.9',
        }

        self.url = "https://serpapi.com/search"
        self.client = Client(api_key=os.getenv("SERPAPI_API_KEY"))

    @log_decorator()
    async def get_legosets_rating(self, legoset_id: str):
        """
        Функция используя API SearchAPI возвращает гугл рейтинг набора если он есть
        :return: str || None
        """
        params = {
            "engine": "google",
            "q": f"Lego {legoset_id}",
            "api_key": "fb4e71f81d0755130f77d3ba2fe5e69a81a0b6fcd7917b6c5d74e9feb057e13a"
        }
        search = self.client.search(params=params)
        result = search.as_dict()
        return result.get('product_result').get('reviews_results').get('user_reviews').get('rating')
        # ic(result.get('organic_results')[0].get('source').keys())