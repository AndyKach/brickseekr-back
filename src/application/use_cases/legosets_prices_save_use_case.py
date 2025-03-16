from application.repositories.prices_repository import LegosetsPricesRepository
from domain.legosets_price import LegosetsPrice
from domain.legosets_prices import LegosetsPrices

import logging
system_logger = logging.getLogger('system_logger')

class LegosetsPricesSaveUseCase:
    def __init__(self,
                 legosets_prices_repository: LegosetsPricesRepository
                 ):
        self.legosets_prices_repository = legosets_prices_repository

    async def save_legosets_price(self, legosets_price: LegosetsPrice):
        """
        Функция сохраняет новую цену на лего набор и в зависимости от того, существует ли на набор уже другие цены
        или нет, сохраняет новую цену или создает новый объект в бд
        """
        log_text = f"\n==================\n"\
                   f"ID: {legosets_price.legoset_id} \n"\
                   f"Price: {legosets_price.price}\n"

        if await self.legosets_prices_repository.get_item(
                legoset_id=legosets_price.legoset_id,
        ) is not None:
            try:
                await self.legosets_prices_repository.save_price(
                    legoset_id=legosets_price.legoset_id,
                    price=legosets_price.price,
                    website_id=legosets_price.website_id
                )
                log_text += f"---Save new items price successfully---"
            except Exception as e:
                system_logger.error(log_text + f"Error by save new price: {e}")
        else:
            try:
                await self.legosets_prices_repository.add_items(
                    LegosetsPrices(
                        legoset_id=legosets_price.legoset_id,
                        prices={legosets_price.website_id: legosets_price.price}
                    )
                )
                log_text += f"~~~Add new item successfully~~~"
            except Exception as e:
                system_logger.error(log_text + f"Error by add new lego set price {e}")

        system_logger.info(log_text)

    async def delete_legosets_price(self, legoset_id: str, website_id: str):
        """
        Функция удаляет цену в БД на конкретный магазин если например цена больше не доступна
        """
        log_text = f"\n==================\n"\
                   f"ID: {legoset_id} \n"\
                   f"Not more available"
        system_logger.info(log_text)
        if await self.legosets_prices_repository.get_item(legoset_id=legoset_id) is not None:
            await self.legosets_prices_repository.delete_price(legoset_id=legoset_id, website_id=website_id)

