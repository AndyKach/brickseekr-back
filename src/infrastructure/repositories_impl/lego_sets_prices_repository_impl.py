from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, text, update

from application.repositories.prices_repository import LegoSetsPricesRepository
from domain.lego_sets_prices import LegoSetsPrices
from infrastructure.db.base import async_engine
from infrastructure.db.models.lego_sets_orm import LegoSetsOrm
from infrastructure.db.models.prices_orm import LegoSetsPricesOrm


class LegoSetsPricesRepositoryImpl(LegoSetsPricesRepository):
    def get_session(self) :
        return AsyncSession(bind=async_engine, expire_on_commit=False)

    async def save_price(self, item_id: str, website_id: str, price: str) -> None:
        session = self.get_session()
        async with session.begin():
            query = (
                select(LegoSetsPricesOrm.prices)
                .where(LegoSetsPricesOrm.lego_set_id == item_id)
            )
            res = await session.execute(query)
            prices = res.scalars().first()

            prices[website_id] = price
            query = (
                update(LegoSetsPricesOrm)
                .where(LegoSetsPricesOrm.lego_set_id == item_id)
                .values(prices=prices)
            )
            await session.execute(query)
            await session.commit()
            # await session.get(LegoSetsPricesOrm)

    async def get_item_all_prices(self, item_id: str) -> dict:
        session = self.get_session()
        async with session.begin():
            query = select(LegoSetsPricesOrm).where(LegoSetsPricesOrm.lego_set_id == item_id)
            res = await session.execute(query)
            if res:
                lego_set_prices_orm = res.scalars()
                lego_set_prices = lego_set_prices_orm.prices
                # lego_set_price = LegoSetsPrices(
                #     price_id=lego_set_price_orm.price_id,
                #     lego_set_id=lego_set_price_orm.lego_set_id,
                #     prices=lego_set_price_orm.prices,
                #     created_at=lego_set_price_orm.created_at
                # )
                return lego_set_prices

    async def get_item_price(self, item_id: str, website_id: str) -> str:
        session = self.get_session()
        async with session.begin():
            query = select(LegoSetsPricesOrm.prices).where(LegoSetsPricesOrm.lego_set_id == item_id)
            res = await session.execute(query)
            if res:
                lego_set_price = res.scalars().first()
                # print(lego_set_price)
                return lego_set_price.get(website_id)

    async def get_all_items(self):
        session = self.get_session()

        async with session.begin():
            query = select(LegoSetsPricesOrm)
            res = await session.execute(query)
            lego_sets_orm = res.scalars().all()
            lego_sets_prices = [
                LegoSetsPrices(
                    lego_set_id=lego_set.lego_set_id,
                    prices=lego_set.prices,
                    created_at=lego_set.created_at
                ) for lego_set in lego_sets_orm]

            return lego_sets_prices

    async def add_item(self, lego_sets_prices: LegoSetsPrices):
        session = self.get_session()
        lego_sets_prices_orm = LegoSetsPricesOrm(
            lego_set_id=lego_sets_prices.lego_set_id,
            prices=lego_sets_prices.prices
        )
        async with session.begin():
            session.add(lego_sets_prices_orm)
            await session.commit()


if __name__ == '__main__':
    price_repository = LegoSetsPricesRepositoryImpl()


