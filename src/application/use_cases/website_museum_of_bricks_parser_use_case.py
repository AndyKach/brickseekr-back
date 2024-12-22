import logging

from application.interfaces.website_interface import WebsiteInterface
from application.repositories.lego_sets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
import aiohttp
import asyncio
from aiolimiter import AsyncLimiter
from aiohttp.client_exceptions import TooManyRedirects

from domain.lego_sets_prices import LegoSetsPrices

system_logger = logging.getLogger('system_logger')

class WebsiteMuseumOfBricksParserUseCase:
    def __init__(self,
                 lego_sets_repository: LegoSetsRepository,
                 lego_sets_prices_repository: LegoSetsPricesRepository,
                 website_interface: WebsiteInterface,
                 ):
        self.lego_sets_repository = lego_sets_repository
        self.lego_sets_prices_repository = lego_sets_prices_repository
        self.website_interface = website_interface

        self.website_id = "4"

    async def parse_lego_sets_url(self, lego_set_id: str = "75257"):
        lego_set_url = await self.website_interface.parse_lego_sets_url()
        await self.lego_sets_repository.update_url_name(lego_set_id=lego_set_id, url_name=lego_set_url)

    async def parse_lego_sets_urls(self):
        lego_sets = await self.lego_sets_repository.get_all()
        for i in range(120, 5745, 100):
            result = await self.website_interface.parse_lego_sets_urls(lego_sets=lego_sets[i:i+100])
        # print('!!!!!!!\n{result}\n!!!!!!!'.format(result=result))
            for lego_set in result:
                await self.lego_sets_repository.update_url_name(
                    lego_set_id=lego_set["id"], url_name=lego_set['url']
                )

    async def parse_lego_sets_price(self, lego_set_id: str):
        lego_set = await self.lego_sets_repository.get_set(set_id=lego_set_id)
        result = await self.website_interface.parse_lego_sets_price(lego_set=lego_set)
        system_logger.info(f"Lego set {lego_set.lego_set_id} - {result}")
        await self.lego_sets_prices_repository.save_price(
            item_id=lego_set.lego_set_id, price=result.get('price'), website_id=self.website_id
        )
        return result

    async def parse_lego_sets_prices(self):
        lego_sets = await self.lego_sets_repository.get_all()
        for i in range(1, len(lego_sets), 100):
            results = await self.website_interface.parse_lego_sets_prices(lego_sets=lego_sets[i:i+100])
            system_logger.info(f"Result: {results}")

            for result in results:
                if result is not None:
                    if await self.lego_sets_prices_repository.get_item(
                            item_id=result.get('lego_set_id'),
                    ) is not None:
                        await self.lego_sets_prices_repository.save_price(
                            item_id=result.get('lego_set_id'),
                            price=result.get('price'),
                            website_id=self.website_id
                        )
                    else:
                        await self.lego_sets_prices_repository.add_item(
                            LegoSetsPrices(
                                lego_set_id=result.get('lego_set_id'),
                                prices={self.website_id: result.get('price')}
                            )
                        )




