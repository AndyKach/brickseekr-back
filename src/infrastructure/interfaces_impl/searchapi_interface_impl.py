import os

from icecream import ic
from serpapi import Client
import serpapi
import sys
from application.interfaces.searchapi_interface import SearchAPIInterface
from infrastructure.config.logs_config import log_decorator


class SearchAPIInterfaceImpl(SearchAPIInterface):
    def __init__(self):
        pass

    @log_decorator()
    async def get_rating(self, legoset_id: str):
        pass
