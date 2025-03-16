import os

from icecream import ic
from serpapi import Client
import serpapi
import sys
from application.interfaces.searchapi_interface import SearchAPIInterface
from infrastructure.config.logs_config import log_decorator


class SearchAPIInterfaceImpl(SearchAPIInterface):
    def __init__(self):
        self.url = "https://serpapi.com/search"
        self.client = Client(api_key=os.getenv("SERPAPI_API_KEY"))

    @log_decorator()
    async def get_rating(self, legoset_id: str):
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