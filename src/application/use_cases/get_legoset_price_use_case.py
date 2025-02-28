import logging

from application.repositories.prices_repository import LegoSetsPricesRepository
from domain.legosets_prices import LegoSetsPrices
from domain.legosets_price import LegoSetsPrice

system_logger = logging.getLogger('system_logger')

class GetLegoSetPriceUseCase:
    def __init__(self,
                 legosets_prices_repository: LegoSetsPricesRepository
                 ):
        self.legosets_prices_repository = legosets_prices_repository

    async def get_all_prices(self, legoset_id: str):
        legoset_prices = await self.legosets_prices_repository.get_item_all_prices(legoset_id=legoset_id)

        if legoset_prices:
            for website_id, value in legoset_prices.prices.items():
                if '€' in value:
                    price = float(value[:value.find(' ')].replace(',', '.'))
                    # print("!!", price)
                    new_value = f"{str(price * 24)[:str(price * 24).find('.')].replace('.', ',')} Kč"
                    system_logger.info(f'For legoset {legoset_id} PRICE OLD: {value} NEW: {new_value}')
                    legoset_prices.prices[website_id] = new_value
                    # await self.legosets_prices_repository.save_price(legoset_id=legoset_id, price=f"{new_value} Kč",
                    #                                                  website_id=website_id)
            return await self.validate_legoset_price_obj(legoset_price=legoset_prices)

    async def get_website_price(self, legoset_id: str, website_id: str):
        legoset_price = await self.legosets_prices_repository.get_item_price(legoset_id=legoset_id, website_id=website_id)
        if legoset_price:
            if '€' in legoset_price.price:
                price = float(legoset_price.price[:legoset_price.price.find(' ')].replace(',', '.'))
                new_value = f"{str(price * 24)[:str(price * 24).find('.')].replace('.', ',')} Kč"
                system_logger.info(f'For legoset {legoset_id} PRICE OLD: {legoset_price.price} NEW: {new_value}')
                legoset_price.price = new_value

            return await self.validate_legoset_price_obj(legoset_price=legoset_price)


    @staticmethod
    async def validate_legoset_price_obj(legoset_price):
        legoset_price.created_at = legoset_price.created_at.isoformat()
        return legoset_price


