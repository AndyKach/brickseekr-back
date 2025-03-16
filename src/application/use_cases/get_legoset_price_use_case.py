import logging

from icecream import ic

from application.controllers.website_controller import WebsiteController
from application.interfaces.website_data_source_interface import WebsiteDataSourceInterface
from application.repositories.prices_repository import LegoSetsPricesRepository
from application.use_cases.website_parser_use_case import WebsiteParserUseCase
from domain.legoset import Legoset
from domain.legosets_prices import LegoSetsPrices
from domain.legosets_price import LegoSetsPrice
from infrastructure.config.logs_config import log_decorator

system_logger = logging.getLogger('system_logger')

class GetLegoSetsPricesUseCase:
    def __init__(self,
                 legosets_prices_repository: LegoSetsPricesRepository,
                 ):
        self.legosets_prices_repository = legosets_prices_repository

    @log_decorator(print_kwargs=True)
    async def get_all_prices(self, legoset_id: str) -> LegoSetsPrices:
        """
        Функция возвращает все цены на набор
        """
        legoset_prices = await self.legosets_prices_repository.get_item_all_prices(legoset_id=legoset_id)

        if legoset_prices:
            return await self.validate_legoset_price_obj(legoset_price=legoset_prices)

    async def get_website_price(self, legoset_id: str, website_id: str):
        """
        Функция возвращает цену на набор в конкретном магазине
        """
        legoset_price = await self.legosets_prices_repository.get_item_price(legoset_id=legoset_id, website_id=website_id)
        if legoset_price:
            return await self.validate_legoset_price_obj(legoset_price=legoset_price)

    @staticmethod
    async def validate_legoset_price_obj(legoset_price):
        """
        Функция изменяет объект даты в текст
        """
        legoset_price.created_at = legoset_price.created_at.isoformat()
        return legoset_price


