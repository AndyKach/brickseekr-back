import logging
from xml.dom.expatbuilder import theDOMImplementation

from icecream import ic

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
                 ):
        self.rating_calculation = RatingCalculation()
        self.legosets_repository = legosets_repository
        self.legosets_prices_repository = legosets_prices_repository

    async def execute(self, legoset_id: str):
        legoset = await self.legosets_repository.get_set(set_id=legoset_id)
        legosets_prices = await self.legosets_prices_repository.get_item_all_prices(legoset_id=legoset_id)
        # ic(legoset)
        # ic(legosets_prices)
        if legosets_prices is not None and legoset.theme is not None and legoset.pieces is not None:
            final_price = 0
            prices_count = 0
            initial_price = 0
            prices = []
            theme = ''
            if legosets_prices.prices.get("1") is not None:
                if "€" not in legosets_prices.prices.get("1") and "\u20ac" not in legosets_prices.prices.get("1"):
                    initial_price = float(legosets_prices.prices.get("1").replace('Kč', '').replace(' ','').replace(',', '.')) / 25.13

                else:
                    initial_price = float(legosets_prices.prices.get("1").replace('€', '').replace(' ','').replace(',', '.'))
                    final_price += initial_price * 25.13
            ic(initial_price)

            for i in range(2, 6):
                ic(legosets_prices.prices.get(str(i)))
                price = legosets_prices.prices.get(str(i))
                if price is not None:
                    price_reformated = float(price.replace('Kč', '').replace(' ','').replace(',', '.'))
                    ic(price_reformated)
                    prices_count += 1
                    final_price += price_reformated
                    prices.append(price_reformated)

            if legoset.theme is not None:
                theme = legoset.theme.lower().replace(' ', '-')
                ic(theme)

            await self.rating_calculation.calculate_rating(
                final_price=final_price,
                initial_price=initial_price,
                years_since_release=2025-int(legoset.year),
                theme=theme,
                pieces_count=legoset.pieces,
                official_price=initial_price,
                best_ratio=min(prices),
                worst_ratio=max(prices),
                rarity_type="Regular Set"
            )

        else:
            system_logger.info(f"Legoset {legoset_id} can't be calculated")
            return {"status_code": 500, "message": f"Legoset {legoset_id} can't be calculated because it's not enough data"}



