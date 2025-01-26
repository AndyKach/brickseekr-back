from application.repositories.prices_repository import LegoSetsPricesRepository
from domain.legosets_prices import LegoSetsPrices
from domain.legosets_price import LegoSetsPrice


class GetLegoSetPriceUseCase:
    def __init__(self,
                 legosets_prices_repository: LegoSetsPricesRepository
                 ):
        self.legosets_prices_repository = legosets_prices_repository

    async def get_all_prices(self, legoset_id: str):
        legoset_prices = await self.legosets_prices_repository.get_item_all_prices(legoset_id=legoset_id)
        if legoset_prices:
            return await self.validate_legoset_price_obj(legoset_price=legoset_prices)

    async def get_website_price(self, legoset_id: str, website_id: int):
        legoset_price = await self.legosets_prices_repository.get_item_price(legoset_id=legoset_id, website_id=website_id)
        print(legoset_price)
        if legoset_price:
            return await self.validate_legoset_price_obj(legoset_price=legoset_price)

    @staticmethod
    async def validate_legoset_price_obj(legoset_price):
        legoset_price.created_at = legoset_price.created_at.isoformat()
        return legoset_price


