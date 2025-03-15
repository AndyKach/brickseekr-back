import logging

from icecream import ic

from application.controllers.website_controller import WebsiteController
from application.interfaces.website_data_source_interface import WebsiteDataSourceInterface
from application.repositories.prices_repository import LegoSetsPricesRepository
from application.use_cases.website_parser_use_case import WebsiteParserUseCase
from domain.legoset import LegoSet
from domain.legosets_prices import LegoSetsPrices
from domain.legosets_price import LegoSetsPrice
from infrastructure.config.logs_config import log_decorator

system_logger = logging.getLogger('system_logger')

class GetLegoSetPriceUseCase:
    def __init__(self,
                 legosets_prices_repository: LegoSetsPricesRepository,
                 website_lego_interface: WebsiteDataSourceInterface,
                 ):
        self.legosets_prices_repository = legosets_prices_repository
        self.website_lego_interface = website_lego_interface

    @log_decorator(print_kwargs=True)
    async def get_all_prices(self, legoset_id: str):
        legoset_prices = await self.legosets_prices_repository.get_item_all_prices(legoset_id=legoset_id)

        if legoset_prices:
            for website_id, value in legoset_prices.prices.items():
                if '€' in value or "valid from" in value:
                    new_price = await self.get_legoset_new_initial_price(legoset_id=legoset_id)
                    system_logger.info(f'For legoset {legoset_id} PRICE OLD: {value} NEW: {new_price}')
                    legoset_prices.prices[website_id] = new_price
                    await self.legosets_prices_repository.save_price(
                        legoset_id=legoset_id,
                        price=f"{new_price} Kč",
                        website_id=website_id
                    )
            return await self.validate_legoset_price_obj(legoset_price=legoset_prices)
        else:
            new_price = await self.get_legoset_new_initial_price(legoset_id=legoset_id)
            if new_price:
                system_logger.info(f'For legoset {legoset_id} PRICE NEW: {new_price}')
                legoset_prices = LegoSetsPrices(legoset_id=legoset_id, prices={"1": f"{new_price} Kč"})
                await self.legosets_prices_repository.add_items(legoset_prices)
                return await self.validate_legoset_price_obj(legoset_price=legoset_prices)

    async def get_website_price(self, legoset_id: str, website_id: str, website_controller: WebsiteController):
        legoset_price = await self.legosets_prices_repository.get_item_price(legoset_id=legoset_id, website_id=website_id)
        ic(legoset_price)
        if legoset_price:
            if legoset_price.price == "-":
                new_price = await website_controller.parse_legosets_price(legoset_id=legoset_id)
                system_logger.info(f'For legoset {legoset_id} FOR WEBSITE {website_id} PRICE NEW: {new_price} ')

            if '€' in legoset_price.price or "valid from" in legoset_price.price:
                new_price = await self.get_legoset_new_initial_price(legoset_id=legoset_id)
                if new_price:
                    system_logger.info(f'For legoset {legoset_id} PRICE OLD: {legoset_price.price} NEW: {new_price}')
                    legoset_price.price = f"{new_price} Kč"
                    await self.legosets_prices_repository.save_price(
                        legoset_id=legoset_id,
                        price=f"{new_price} Kč",
                        website_id=website_id
                    )



            return await self.validate_legoset_price_obj(legoset_price=legoset_price)

        elif website_id == "1":
            new_price = await self.get_legoset_new_initial_price(legoset_id=legoset_id)
            if new_price:
                system_logger.info(f'For legoset {legoset_id} PRICE NEW: {new_price}')
                legoset_prices = LegoSetsPrices(legoset_id=legoset_id, prices={"1": f"{new_price} Kč"})
                await self.legosets_prices_repository.add_items(legoset_prices)
                return await self.validate_legoset_price_obj(legoset_price=legoset_prices)


    async def get_legoset_new_initial_price(self, legoset_id: str):
        new_value = await self.website_lego_interface.parse_legosets_price(legoset=legoset_id)
        system_logger.info(new_value)
        return new_value.get('price')

    @staticmethod
    async def validate_legoset_price_obj(legoset_price):
        legoset_price.created_at = legoset_price.created_at.isoformat()
        return legoset_price


