import logging
from datetime import datetime
from xml.dom.expatbuilder import theDOMImplementation
from statistics import median

from icecream import ic

from application.interfaces.google_interface import GoogleInterface
from application.interfaces.searchapi_interface import SearchAPIInterface
from application.interfaces.website_data_source_interface import WebsiteDataSourceInterface
from application.repositories.legosets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from domain.legoset import LegoSet
from domain.legosets_prices import LegoSetsPrices
from domain.rating_calculation import RatingCalculation
from infrastructure.config.logs_config import log_decorator

system_logger = logging.getLogger('system_logger')

class LegoSetsRatingUseCase:
    def __init__(self,
                 legosets_repository: LegoSetsRepository,
                 legosets_prices_repository: LegoSetsPricesRepository,
                 search_api_interface: SearchAPIInterface,
                 google_interface: GoogleInterface,
                 ):
        self.rating_calculation = RatingCalculation()
        self.legosets_repository = legosets_repository
        self.legosets_prices_repository = legosets_prices_repository
        self.search_api_interface = search_api_interface
        self.google_interface = google_interface

    async def execute(self, legoset: LegoSet):
        """
        Calculate legosets rating

        :param legoset: LegoSet obj
        :return: {'status_code': int, 'rating': float}
        """
        legosets_prices = await self.legosets_prices_repository.get_item_all_prices(legoset_id=legoset.id)

        # -------------------------------------------------------------------------------------------------------------
        if legoset.google_rating is None:
            await self.google_interface.open_driver()
            google_rating = await self.google_interface.get_legosets_rating(legoset_id=legoset.id)
            # google_rating = await self.search_api_interface.get_rating(legoset_id=legoset.id)

            await self.google_interface.close_driver()

            if google_rating is None:
                system_logger.error(f"Legoset: {legoset.id} has no GOOGLE RATING. Rating calculation is not possible")
                return await self.get_error_code(legoset_id=legoset.id)
            else:
                legoset.google_rating = google_rating
                await self.legosets_repository.update_google_rating(legoset_id=legoset.id, google_rating=google_rating)
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
                # years_since_release=years_since_release,
                theme=theme,
                pieces_count=pieces_count,
                # best_ratio=best_ratio,
                # worst_ratio=worst_ratio,
                google_rating=google_rating,
            )
            result = {
                "status_code": 200,
                "message": f"Legoset {legoset.id} have rating {rating}",
                "rating": rating,
                "legoset_id": legoset.id,
            }
            return result

        else:
            system_logger.info(f"Legoset {legoset.id} can't be calculated but it has google rating {google_rating}")
            system_logger.info(f"Legoset {legoset.id} prices: {legosets_prices}, theme: {legoset.theme}, pieces: {legoset.pieces}")
            result = {
                "status_code": 206,
                "message": f"Legoset {legoset.id} can't be calculated because it's not enough data but google rating can be send back",
                "google_rating": google_rating,
                "legoset_id": legoset.id,

            }
            return result

    @staticmethod
    async def refactor_price_from_str_to_float(price: str) -> float:
        return float(price.replace(' ', '').replace(',', '.').replace('Kč', ''))

    @staticmethod
    async def get_error_code(legoset_id: str) -> dict:
        return {
            "status_code": 500,
            "message": f"Legoset {legoset_id} can't be calculated because it's not enough data",
            "legoset_id": legoset_id,
        }

    @log_decorator()
    async def recalculate_all_legosets(self):
        """
        Функция пересчитывает все лего наборы
        """
        # legosets = [legoset for legoset in await self.legosets_repository.get_all() if legoset.rating > 5]
        legosets = [legoset for legoset in await self.legosets_repository.get_all()]
        system_logger.info(f"Legosets count to recalculate: {len(legosets)}")
        for legoset in legosets:
            await self.recalculate_legoset(legoset=legoset)

    @log_decorator()
    async def recalculate_legoset(self, legoset: LegoSet):
        system_logger.info(f"Start recalculating legoset: {legoset.id}")
        result = await self.execute(legoset=legoset)
        if result:
            await self.__save_new_rating(result=result)

    @log_decorator()
    async def __save_new_rating(self, result: dict):
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



