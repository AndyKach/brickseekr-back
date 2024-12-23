from application.repositories.prices_repository import LegoSetsPricesRepository
from domain.lego_sets_price import LegoSetsPrice
from domain.lego_sets_prices import LegoSetsPrices


class LegoSetsPricesSaveUseCase:
    def __init__(self,
                 lego_sets_prices_repository: LegoSetsPricesRepository
                 ):
        self.lego_sets_prices_repository = lego_sets_prices_repository

    async def save_lego_sets_price(self, lego_set_price: LegoSetsPrice):
        if await self.lego_sets_prices_repository.get_item(
                lego_set_id=lego_set_price.lego_set_id,
        ) is not None:
            await self.lego_sets_prices_repository.save_price(
                lego_set_id=lego_set_price.lego_set_id,
                price=lego_set_price.price,
                website_id=lego_set_price.website_id
            )
        else:
            await self.lego_sets_prices_repository.add_item(
                LegoSetsPrices(
                    lego_set_id=lego_set_price.lego_set_id,
                    prices={lego_set_price.website_id: lego_set_price.price}
                )
            )