import logging
from datetime import datetime
from statistics import median

from icecream import ic

from application.controllers.website_brickset_controller import WebsiteBricksetController
from application.interfaces.searchapi_interface import SearchAPIInterface
from application.repositories.legosets_repository import LegosetsRepository
from application.repositories.prices_repository import LegosetsPricesRepository
from application.repositories.websites_repository import WebsitesRepository
from application.use_cases.get_legoset_price_use_case import GetLegosetsPricesUseCase
from application.use_cases.legosets_rating_use_case import LegosetsRatingUseCase
from application.use_cases.get_website_use_case import GetWebsiteUseCase
from domain.legoset import Legoset
from domain.rating_calculation import RatingCalculation
from infrastructure.config.logs_config import log_decorator

system_logger = logging.getLogger('system_logger')
class GetLegosetUseCase:
    def __init__(self,
                 legosets_repository: LegosetsRepository,
                 legosets_prices_repository: LegosetsPricesRepository,
                 websites_repository: WebsitesRepository,
                 website_brickset_controller: WebsiteBricksetController,
                 # search_api_interface: SearchAPIInterface,
                 get_legosets_rating_use_case: LegosetsRatingUseCase,
                 get_legosets_prices_use_case: GetLegosetsPricesUseCase,
                 get_website_use_case: GetWebsiteUseCase,
                 ):
        self.legosets_repository = legosets_repository
        self.legosets_prices_repository = legosets_prices_repository
        self.websites_repository = websites_repository
        self.website_brickset_controller = website_brickset_controller

        self.rating_calculation = RatingCalculation()

        self.get_legosets_rating_use_case = get_legosets_rating_use_case
        self.get_legosets_prices_use_case = get_legosets_prices_use_case
        self.get_website_use_case = get_website_use_case

    @log_decorator(print_kwargs=True)
    async def execute(self, legoset_id: str):
        """
        Функция ищет лего набор в базе данных и его цены, и затем сохраняет их особым способом, чтобы было читаемо при запросе API
        """
        result = {}
        legoset = await self.get_legoset(legoset_id=legoset_id)
        if legoset:
            result['legoset'] = legoset
            result['prices'] = await self.get_legosets_prices(legoset_id=legoset_id)
            # ic(result)
            return result
        else:
            return None

    async def get_legoset(self, legoset_id: str):
        """
        Функция ищет легонабор в БД и проверяет нужно ли пересчитать рейтинг
        """
        legoset = await self.legosets_repository.get_set(set_id=legoset_id)
        if legoset:
            legoset = await self.validate_datetime_values(legoset)
            if legoset.rating is None or legoset.rating <= 5:
                await self.__recalculate_legosets_rating(legoset=legoset)
            else:
                system_logger.info(f"Legoset {legoset_id} has rating: {legoset.rating}")
            return legoset
        else:
            return None


    async def get_legosets_prices(self, legoset_id: str):
        """
        Функция ищет цены на легонабор в БД и рефакторит их в читаемый одинаковый стиль
        и также добавляет в возвращаемые данные ссылки на магазины
        """
        result = {}
        legoset_prices = await self.get_legosets_prices_use_case.get_all_prices(legoset_id=legoset_id)
        if legoset_prices:
            for website_id in legoset_prices.prices.keys():
                result[website_id] = {}
                price = self.refactor_price_from_str_to_float(legoset_prices.prices.get(website_id))
                result[website_id]['price'] = price

                website_link = (await self.get_website_use_case.get_website(website_id=website_id)).link
                if website_id == "1":
                    website_link += f'products/{legoset_id}'
                result[website_id]['link'] = website_link

        return result

    @log_decorator(print_kwargs=True)
    async def get_top_list(self, legosets_count: int):
        """
        Функция запрашивает у ДБ рейтинг легонаборов по убывания
        """
        legosets = await self.legosets_repository.get_top_rating(legosets_count=legosets_count)
        # ic(legosets)
        for legoset in legosets:
            await self.validate_datetime_values(legoset)
            # system_logger.info(f"Legoset {legoset.id} has {legoset.rating} rating")
        return legosets

    @staticmethod
    async def validate_datetime_values(legoset: Legoset):
        """
        Так как в БД формат данных для дней и времени отличается от текста, эта функция переводит даты в текст
        """
        if legoset.launchDate:
            legoset.launchDate = legoset.launchDate.isoformat()
        if legoset.exitDate:
            legoset.exitDate = legoset.exitDate.isoformat()
        if legoset.updated_at:
            legoset.updated_at = legoset.updated_at.isoformat()
        if legoset.created_at:
            legoset.created_at = legoset.created_at.isoformat()
        return legoset

    @staticmethod
    def refactor_price_from_str_to_float(price: str) -> str:
        if price.count(' ') > 1:
            price = price.replace(' ', '', price.count(' ') - 1)
        return price

    async def __recalculate_legosets_rating(self, legoset):
        """
        Пересчитывает рейтинг набора и в зависимости от результата сохраняет данные
        """
        try:
            result = await self.get_legosets_rating_use_case.execute(legoset=legoset)
            ic(result)
            match result.get('status_code'):
                case 200:
                    legoset.rating = result.get('rating')
                case 206:
                    legoset.rating = result.get('google_rating') * -1
                    system_logger.info(result.get('message'))
                case 500:
                    system_logger.error(f"Legoset {legoset.id} rating can't be calculated")

            await self.legosets_repository.update_rating(legoset_id=legoset.id, rating=legoset.rating)

        except Exception as e:
            system_logger.error(f"Legoset {legoset.id} has an error: {e}")