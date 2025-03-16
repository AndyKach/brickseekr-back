from abc import ABC, abstractmethod
import asyncio

import logging
from datetime import datetime

from icecream import ic

from application.interfaces.website_interface import WebsiteInterface
from application.repositories.prices_repository import LegosetsPricesRepository
from application.repositories.legosets_repository import LegosetsRepository
from application.use_cases.legosets_prices_save_use_case import LegosetsPricesSaveUseCase
from domain.legoset import Legoset
from domain.legosets_price import LegosetsPrice
from domain.legosets_prices import LegosetsPrices

system_logger = logging.getLogger('system_logger')


class WebsiteParserUseCase(ABC):
    @abstractmethod
    def parse_legosets_price(self, legoset_id: str):
        pass

    @abstractmethod
    def parse_legosets_prices(self):
        pass

    async def _parse_items(
        self, legosets: list[Legoset], website_id: str,
        website_interface: WebsiteInterface, legosets_prices_save_use_case: LegosetsPricesSaveUseCase,
        ):
        """
        Функция парсит цены для всех переданных наборов с шагом 50 наборов в 15 секунд, чтобы сайт не заблокировал за DDOS
        """
        time_start=datetime.now()
        count_valuable = 0
        system_logger.info(f'Count Lego sets: {len(legosets)}')
        for i in range(0, len(legosets), 50):
            system_logger.info(f'Start parse sets from {i} bis {i+50}')
            try:
                results = await website_interface.parse_legosets_prices(legosets=legosets[i:i + 50])
                if results:
                    for result in results:
                        if result:
                            count_valuable += 1
                            await self.__save_new_price(result=result, website_id=website_id,
                                                        legosets_prices_save_use_case=legosets_prices_save_use_case)

            except Exception as e:
                system_logger.error(e)

            system_logger.info(f'Start pause 15s')
            await asyncio.sleep(15)
        system_logger.info(f"Number of successful ones: {count_valuable}")
        system_logger.info(f'Parse is end in {datetime.now()-time_start}')

    async def _parse_item(
        self, legoset: Legoset, website_id: str,
        website_interface: WebsiteInterface, legosets_prices_save_use_case: LegosetsPricesSaveUseCase,
        ):
        """
        Функция парсит цены для конкретного переданного набора
        """
        result = await website_interface.parse_legosets_price(legoset=legoset)
        system_logger.info(f"Lego set {legoset.id} - {result}")
        if result:
            await self.__save_new_price(result=result, website_id=website_id,
                                        legosets_prices_save_use_case=legosets_prices_save_use_case)
        return result


    @staticmethod
    async def __save_new_price(result: dict, website_id: str, legosets_prices_save_use_case: LegosetsPricesSaveUseCase):
        """
        Функция смотрит доступен ли набор еще в магазине или нет, и если не доступен, то удаляет его цену из ДБ
        """
        if result.get('available') == "Retired product":
            await legosets_prices_save_use_case.delete_legosets_price(legoset_id=result.get('legoset_id'), website_id=website_id)
        if result.get('price'):
            await legosets_prices_save_use_case.save_legosets_price(
                LegosetsPrice(
                    legoset_id=result.get('legoset_id'),
                    price=result.get('price'),
                    website_id=website_id
                )
            )
