import logging
from datetime import datetime
from xml.dom.expatbuilder import theDOMImplementation
from statistics import median

from icecream import ic

from application.interfaces.searchapi_interface import SearchAPIInterface
from application.repositories.legosets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from domain.legoset import LegoSet
from domain.legosets_prices import LegoSetsPrices
from domain.rating_calculation import RatingCalculation

system_logger = logging.getLogger('system_logger')

class GetLegoSetsRatingUseCase:
    def __init__(self,
                 legosets_repository: LegoSetsRepository,
                 legosets_prices_repository: LegoSetsPricesRepository,
                 search_api_interface: SearchAPIInterface,
                 ):
        self.rating_calculation = RatingCalculation()
        self.legosets_repository = legosets_repository
        self.legosets_prices_repository = legosets_prices_repository
        self.search_api_interface = search_api_interface

    async def execute(self, legoset: LegoSet):
        legosets_prices = await self.legosets_prices_repository.get_item_all_prices(legoset_id=legoset.id)

        # -------------------------------------------------------------------------------------------------------------

        google_rating = await self.search_api_interface.get_rating(legoset_id=legoset.id)
        if google_rating is None:
            system_logger.error(f"Legoset: {legoset.id} has no GOOGLE RATING. Rating calculation is not possible")

            return await self.get_error_code(legoset_id=legoset.id)

        system_logger.info(f"Legoset: {legoset.id} has a google rating: {google_rating}")

        # -------------------------------------------------------------------------------------------------------------

        if legosets_prices is not None and legoset.theme is not None and legoset.pieces is not None:
            final_price = 0
            prices_count = 0
            initial_price = 0
            prices = []
            theme = ''
            # -------------------------------------------------------------------------------------------------------------
            initial_price_str = legosets_prices.prices.get("1")
            if initial_price_str is not None:
                if "€" in initial_price_str or "\u20ac" in initial_price_str:
                    system_logger.error(f"Legoset: {legoset.id} has a initial price: {initial_price_str} but it is in Euro")

                    return await self.get_error_code(legoset_id=legoset.id)

                else:
                    system_logger.debug(f"Legoset: {legoset.id} has a initial price: {initial_price_str}")

                    initial_price = await self.refactor_price_from_str_to_float(initial_price_str)

                # else:
                #     initial_price = float(legosets_prices.prices.get("1").replace('€', '').replace(' ','').replace(',', '.'))
                #     final_price += initial_price * 25.13

            # -------------------------------------------------------------------------------------------------------------

            prices_list = []
            for website_id in legosets_prices.prices.keys():
                prices_list.append(await self.refactor_price_from_str_to_float(legosets_prices.prices.get(website_id)))

            ic(prices_list)
            ic(median(prices_list))

            final_price = median(prices_list)
            if final_price == 0.0:
                system_logger.error(f"Legoset: {legoset.id} has no PRICES. Rating calculation is not possible")
                return await self.get_error_code(legoset_id=legoset.id)

            system_logger.debug(f"Legoset: {legoset.id} has a final price: {final_price}")

            # -------------------------------------------------------------------------------------------------------------

            years_since_release = datetime.now().year - legoset.year

            system_logger.debug(f"Legoset: {legoset.id} has a years since release: {years_since_release}")

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

            best_ratio = min(prices_list)
            worst_ratio = max(prices_list)
            system_logger.debug(f"Legoset: {legoset.id} has a best ratio: {best_ratio}")
            system_logger.debug(f"Legoset: {legoset.id} has a worst ratio: {worst_ratio}")

            # -------------------------------------------------------------------------------------------------------------

            rating = await self.rating_calculation.calculate_rating(
                final_price=final_price,
                initial_price=initial_price,
                years_since_release=years_since_release,
                theme=theme,
                pieces_count=pieces_count,
                best_ratio=best_ratio,
                worst_ratio=worst_ratio,
                google_rating=google_rating,
            )
            result = {
                "status_code": 200,
                "message": f"Legoset {legoset.id} have rating {rating}",
                "rating": rating
            }
            return result

        else:
            system_logger.info(f"Legoset {legoset.id} can't be calculated but it has google rating {google_rating}")
            result = {
                "status_code": 206,
                "message": f"Legoset {legoset.id} can't be calculated because it's not enough data but google rating can be send back",
                "google_rating": google_rating,

            }
            return result

    @staticmethod
    async def refactor_price_from_str_to_float(price: str) -> float:
        return float(price[:price.rfind(' ')].replace(' ', '').replace(',', '.'))

    @staticmethod
    async def get_error_code(legoset_id: str) -> dict:
        return {
            "status_code": 500,
            "message": f"Legoset {legoset_id} can't be calculated because it's not enough data"
        }


