import logging
from datetime import datetime
from xml.dom.expatbuilder import theDOMImplementation
from statistics import median

from icecream import ic

from application.interfaces.google_interface import GoogleInterface
from application.interfaces.searchapi_interface import SearchAPIInterface
from application.interfaces.website_data_source_interface import WebsiteDataSourceInterface
from application.repositories.legosets_repository import LegosetsRepository
from application.repositories.prices_repository import LegosetsPricesRepository
from domain.legoset import Legoset
from domain.legosets_prices import LegosetsPrices
from domain.rating_calculation import RatingCalculation
from infrastructure.config.logs_config import log_decorator

system_logger = logging.getLogger('system_logger')

class LegosetsRatingUseCase:
    def __init__(self,
                 legosets_repository: LegosetsRepository,
                 legosets_prices_repository: LegosetsPricesRepository,
                 search_api_interface: SearchAPIInterface,
                 google_interface: GoogleInterface,
                 ):
        self.rating_calculation = RatingCalculation()
        self.legosets_repository = legosets_repository
        self.legosets_prices_repository = legosets_prices_repository
        self.search_api_interface = search_api_interface
        self.google_interface = google_interface

    @log_decorator()
    async def recalculate_all_legosets(self):
        """
        Функция пересчитывает все лего наборы
        """
        legosets = [legoset for legoset in await self.legosets_repository.get_all() if legoset.google_rating is not None and legoset.google_rating > 0 and legoset.year > 2022]
        # legosets = [legoset for legoset in await self.legosets_repository.get_all()]
        system_logger.info(f"Legosets count to recalculate: {len(legosets)}")
        for legoset in legosets:
            await self.recalculate_legoset(legoset=legoset)

    @log_decorator()
    async def recalculate_legoset(self, legoset: Legoset):
        """
        Функция пересчитывает конкретный лего набор
        """
        system_logger.info(f"Start recalculating legoset: {legoset.id}")
        result = await self.execute(legoset=legoset)
        if result:
            await self.__save_new_rating(result=result)

    @log_decorator()
    async def __save_new_rating(self, result: dict):
        """
        Функция смотрит какой был результат выполнения расчета рейтинг и в зависимости от статуса выполнения сохрананяет определенные значения
        """
        match result.get('status_code'):
            case 200:
                system_logger.info(result.get('message'))
                await self.legosets_repository.update_rating(legoset_id=result.get("legoset_id"), rating=result.get("rating"))
            case 206:
                system_logger.info(result.get('message'))
                await self.legosets_repository.update_rating(legoset_id=result.get("legoset_id"), rating=0.0)
                await self.legosets_repository.update_google_rating(legoset_id=result.get("legoset_id"),
                                                                    google_rating=result.get("google_rating"))
            case 500:
                system_logger.info(result.get('message'))
                await self.legosets_repository.update_rating(legoset_id=result.get("legoset_id"), rating=0.0)


    async def execute(self, legoset: Legoset):
        """
        Функция расчитывает особые параметры для расчета рейтинга, сохраняет их в отельные переменные
        и проверяет их на корректность и затем передает в особый класс где все расчитывается

        :return:
            If status_code=200:  {'status_code': 200, 'rating': float, 'legoset_id': str};
            If status_code=206:  {'status_code': 206, 'google_rating': float, 'legoset_id': str};
            If status_code=500:  {'status_code': 500, 'legoset_id': str};
        """
        legosets_prices = await self.legosets_prices_repository.get_item_all_prices(legoset_id=legoset.id)

        # -------------------------------------------------------------------------------------------------------------
        if legoset.google_rating is None:
            return await self.get_error_code(legoset_id=legoset.id)
            # await self.google_interface.open_driver()
            # google_rating = await self.google_interface.get_legosets_rating(legoset_id=legoset.id)
            # google_rating = await self.search_api_interface.get_rating(legoset_id=legoset.id)

            # await self.google_interface.close_driver()

            # if google_rating is None:
            #     system_logger.error(f"Legoset: {legoset.id} has no GOOGLE RATING. Rating calculation is not possible")
            #     return await self.get_error_code(legoset_id=legoset.id)
            # else:
            #     legoset.google_rating = google_rating
            #     await self.legosets_repository.update_google_rating(legoset_id=legoset.id, google_rating=google_rating)
        else:
            google_rating = legoset.google_rating


        system_logger.info(f"Legoset: {legoset.id} has a google rating: {google_rating}")

        # -------------------------------------------------------------------------------------------------------------

        if (legoset.theme is not None and legoset.pieces is not None and
                legosets_prices is not None and legosets_prices.prices.get("1") and len(legosets_prices.prices) > 1 ):
            initial_price_str = legosets_prices.prices.get("1")
            if initial_price_str: # legoset have price
                initial_price = await self.refactor_price_from_str_to_float(initial_price_str)
            else: # legoset has no price
                return await self.get_error_code(legoset_id=legoset.id)

            system_logger.debug(f"Legoset: {legoset.id} has a initial price: {initial_price}")

            # -------------------------------------------------------------------------------------------------------------

            prices_list = []
            for website_id in legosets_prices.prices.keys():
                if website_id != "1":
                    prices_list.append(await self.refactor_price_from_str_to_float(legosets_prices.prices.get(website_id)))

            system_logger.debug(f"Legoset: {legoset.id} has a prices_list: {prices_list}")
            system_logger.debug(f"Legoset: {legoset.id} has a median(prices_list): {median(prices_list)}")

            final_price = median(prices_list)
            if final_price == 0.0:
                system_logger.error(f"Legoset: {legoset.id} has no PRICES. Rating calculation is not possible")
                return await self.get_error_code(legoset_id=legoset.id)

            system_logger.debug(f"Legoset: {legoset.id} has a final price: {final_price}")

            # -------------------------------------------------------------------------------------------------------------

            theme = legoset.theme
            if legoset.theme is not None:
                theme = theme.lower().replace(' ', '-')
            else:
                system_logger.error(f"Legoset: {legoset.id} has no THEME. Rating calculation is not possible")
                return await self.get_error_code(legoset_id=legoset.id)

            system_logger.debug(f"Legoset: {legoset.id} has a theme: {theme}")

            # -------------------------------------------------------------------------------------------------------------

            pieces_count = legoset.pieces
            if pieces_count is None:
                system_logger.debug(f"Legoset: {legoset.id} has no PIECES COUNT. Rating calculation is not possible")
                return await self.get_error_code(legoset_id=legoset.id)

            system_logger.debug(f"Legoset: {legoset.id} has a pieces count: {pieces_count}")

            # -------------------------------------------------------------------------------------------------------------

            rating = await self.rating_calculation.calculate_rating(
                final_price=final_price,
                initial_price=initial_price,
                theme=theme,
                pieces_count=pieces_count,
                google_rating=google_rating,
            )
            result = await self.get_rating_success_code(legoset_id=legoset.id, rating=rating)
        else:
            system_logger.info(f"Legoset {legoset.id} can't be calculated but it has google rating {google_rating}")
            system_logger.info(f"Legoset {legoset.id} prices: {legosets_prices}, theme: {legoset.theme}, pieces: {legoset.pieces}")
            result = await self.get_google_rating_success_code(legoset_id=legoset.id, google_rating=google_rating)
        return result

    @staticmethod
    async def refactor_price_from_str_to_float(price: str) -> float:
        return float(price.replace(' ', '').replace(',', '.').replace('Kč', ''))

    @staticmethod
    async def get_rating_success_code(legoset_id: str, rating: float) -> dict:
        return {
                "status_code": 200,
                "message": f"Legoset {legoset_id} have rating {rating}",
                "rating": rating,
                "legoset_id": legoset_id
        }

    @staticmethod
    async def get_google_rating_success_code(legoset_id: str, google_rating: float) -> dict:
        return {
            "status_code": 206,
            "message": f"Legoset {legoset_id} can't be calculated because it's not enough data but google rating can be send back",
            "google_rating": google_rating,
            "legoset_id": legoset_id
        }

    @staticmethod
    async def get_error_code(legoset_id: str) -> dict:
        return {
            "status_code": 500,
            "message": f"Legoset {legoset_id} can't be calculated because it's not enough data",
            "legoset_id": legoset_id
        }


