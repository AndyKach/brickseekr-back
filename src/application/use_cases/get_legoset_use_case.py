import logging
from datetime import datetime
from statistics import median

from icecream import ic

from application.controllers.website_brickset_controller import WebsiteBricksetController
from application.interfaces.searchapi_interface import SearchAPIInterface
from application.repositories.legosets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from application.use_cases.get_legosets_rating_use_case import GetLegoSetsRatingUseCase
from domain.legoset import LegoSet
from domain.rating_calculation import RatingCalculation
from infrastructure.config.logs_config import log_decorator

system_logger = logging.getLogger('system_logger')
class GetLegoSetUseCase:
    def __init__(self,
                 legosets_repository: LegoSetsRepository,
                 legosets_prices_repository: LegoSetsPricesRepository,
                 website_brickset_controller: WebsiteBricksetController,
                 # search_api_interface: SearchAPIInterface,
                 get_legosets_rating_use_case: GetLegoSetsRatingUseCase,
                 ):
        self.legosets_repository = legosets_repository
        self.legosets_prices_repository = legosets_prices_repository
        self.website_brickset_controller = website_brickset_controller

        self.rating_calculation = RatingCalculation()

        self.get_legosets_rating_use_case = get_legosets_rating_use_case

    @log_decorator(print_kwargs=True)
    async def execute(self, legoset_id: str):
        legoset = await self.legosets_repository.get_set(set_id=legoset_id)
        if legoset:
            legoset = await self.validate_datetime_values(legoset)
            if legoset.rating is None or legoset.rating <= 5:
                legoset.rating = 0
                # system_logger.info(f"Legoset {legoset_id} has no yet official rating")
                try:
                    result = await self.get_legosets_rating_use_case.execute(legoset=legoset)
                    match result.get('status_code'):
                        case 200:
                            legoset.rating = result.get('rating')
                        case 206:
                            legoset.rating = result.get('google_rating') * -1
                        case 500:
                            system_logger.error(f"Legoset {legoset_id} rating can't be calculated")

                    await self.legosets_repository.update_rating(legoset_id=legoset.id, rating=legoset.rating)
                    # await self.get_rating(legoset=legoset)
                except AttributeError:
                    system_logger.error(f"Legoset {legoset_id} has no google rating")

                except Exception as e:
                    system_logger.error(f"Legoset {legoset_id} has an error: {e}")
            else:
                system_logger.info(f"Legoset {legoset_id} has rating: {legoset.rating}")
        else:
            pass
            # TODO Если нет информации чекнуть на brickset о информации
            #  1. спарсить, сохранить, вернуть
            # await self.website_brickset_parser_use_case.parse
        return legoset

    @log_decorator(print_kwargs=True)
    async def get_top_list(self, legosets_count: int):
        legosets = await self.legosets_repository.get_top_rating(legosets_count=legosets_count)
        # ic(legosets)
        for legoset in legosets:
            await self.validate_datetime_values(legoset)
            system_logger.info(f"Legoset {legoset.id} has {legoset.rating} rating")
        return legosets

    @staticmethod
    async def validate_datetime_values(legoset: LegoSet):
        if legoset.launchDate:
            legoset.launchDate = legoset.launchDate.isoformat()
        if legoset.exitDate:
            legoset.exitDate = legoset.exitDate.isoformat()
        if legoset.updated_at:
            legoset.updated_at = legoset.updated_at.isoformat()
        if legoset.created_at:
            legoset.created_at = legoset.created_at.isoformat()
        return legoset


    # async def get_rating(self, legoset: LegoSet):
    #     legoset_prices = await self.legosets_prices_repository.get_item_all_prices(legoset_id=legoset.id)
    #
    #     if legoset_prices.prices.get('1') is not None:
    #         initial_price = self.refactor_price_from_str_to_float(legoset_prices.prices.get('1'))
    #     else:
    #         system_logger.info(f"Legoset: {legoset.id} has no INITIAL PRICE. Rating calculation is not possible")
    #         return -1
    #
    #     system_logger.info(f"Legoset: {legoset.id} has a initial price: {initial_price}")
    #
    #     # -------------------------------------------------------------------------------------------------------------
    #
    #     final_price = 0.0
    #     prices_list = []
    #     for website_id in legoset_prices.prices.keys():
    #         prices_list.append(self.refactor_price_from_str_to_float(legoset_prices.prices.get(website_id)))
    #         # final_price += prices_list[-1]
    #         # prices_list
    #         # median(prices_list)
    #
    #     final_price = median(prices_list) / len(legoset_prices.prices.keys())
    #     if final_price == 0.0:
    #         system_logger.info(f"Legoset: {legoset.id} has no PRICES. Rating calculation is not possible")
    #         return -1
    #
    #     system_logger.info(f"Legoset: {legoset.id} has a final price: {final_price}")
    #
    #     # -------------------------------------------------------------------------------------------------------------
    #
    #     years_since_release = datetime.now().year - legoset.year
    #
    #     system_logger.info(f"Legoset: {legoset.id} has a years since release: {years_since_release}")
    #
    #
    #     # -------------------------------------------------------------------------------------------------------------
    #
    #     theme = legoset.theme
    #     if theme is None:
    #         system_logger.info(f"Legoset: {legoset.id} has no THEME. Rating calculation is not possible")
    #         return -1
    #
    #     system_logger.info(f"Legoset: {legoset.id} has a theme: {theme}")
    #
    #     # -------------------------------------------------------------------------------------------------------------
    #
    #     pieces_count = legoset.pieces
    #     if pieces_count is None:
    #         system_logger.info(f"Legoset: {legoset.id} has no PIECES COUNT. Rating calculation is not possible")
    #         return -1
    #
    #     system_logger.info(f"Legoset: {legoset.id} has a pieces count: {pieces_count}")
    #
    #
    #     # -------------------------------------------------------------------------------------------------------------
    #
    #     best_ratio = min(prices_list)
    #     worst_ratio = max(prices_list)
    #     system_logger.info(f"Legoset: {legoset.id} has a best ratio: {best_ratio}")
    #     system_logger.info(f"Legoset: {legoset.id} has a worst ratio: {worst_ratio}")
    #
    #
    #
    #     # -------------------------------------------------------------------------------------------------------------
    #
    #     rarity_type = "Regular Set"
    #     system_logger.info(f"Legoset: {legoset.id} has a final price: {rarity_type}")
    #
    #
    #     # -------------------------------------------------------------------------------------------------------------
    #
    #     google_rating = self.search_api_interface.get_rating(legoset_id=legoset.id)
    #     system_logger.info(f"Legoset: {legoset.id} has a google rating: {google_rating}")
    #
    #
    #     # -------------------------------------------------------------------------------------------------------------
    #
    #     await self.rating_calculation.calculate_rating(
    #         final_price=final_price,
    #         initial_price=initial_price,
    #         years_since_release=years_since_release,
    #         theme=theme,
    #         pieces_count=pieces_count,
    #         best_ratio=best_ratio,
    #         worst_ratio=worst_ratio,
    #         rarity_type=rarity_type,
    #         google_rating=google_rating,
    #     )

    def refactor_price_from_str_to_float(self, price: str) -> float:
        return float(price[:price.find(' ')].replace(',', '.'))

