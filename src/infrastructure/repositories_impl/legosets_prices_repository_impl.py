from icecream import ic
from pydantic.v1 import NoneIsNotAllowedError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, text, update, func, cast
from sqlalchemy.dialects.postgresql import JSONB

from application.repositories.prices_repository import LegoSetsPricesRepository
from domain.legosets_price import LegoSetsPrice
from domain.legosets_prices import LegoSetsPrices
from infrastructure.config.logs_config import log_decorator
from infrastructure.db.base import async_engine
from infrastructure.db.models.legosets_orm import LegoSetsOrm
from infrastructure.db.models.legosets_prices_orm import LegoSetsPricesOrm


class LegoSetsPricesRepositoryImpl(LegoSetsPricesRepository):
    @staticmethod
    def get_session() :
        return AsyncSession(bind=async_engine, expire_on_commit=False)

    @log_decorator(print_args=False)
    async def save_price(self, legoset_id: str, website_id: str, price: str) -> None:
        session = self.get_session()
        async with session.begin():
            query = (
                select(LegoSetsPricesOrm.prices)
                .where(LegoSetsPricesOrm.legoset_id == legoset_id)
            )
            res = await session.execute(query)
            prices = res.scalars().first()
            prices[website_id] = price

            query = (
                update(LegoSetsPricesOrm)
                .where(LegoSetsPricesOrm.legoset_id == legoset_id)
                .values(prices=prices)
            )
            await session.execute(query)
            await session.commit()

    @log_decorator(print_args=False)
    async def get_item_all_prices(self, legoset_id: str) -> LegoSetsPrices | None:
        session = self.get_session()
        async with session.begin():
            query = select(LegoSetsPricesOrm).where(LegoSetsPricesOrm.legoset_id == legoset_id)
            res = await session.execute(query)
            if res:
                legoset_prices_orm = res.scalars().first()
                if legoset_prices_orm:
                    return LegoSetsPrices(
                        legoset_id=legoset_prices_orm.legoset_id,
                        prices=legoset_prices_orm.prices,
                        created_at=legoset_prices_orm.created_at,
                    )

    @log_decorator(print_args=False)
    async def get_item_price(self, legoset_id: str, website_id: str) -> LegoSetsPrice | None:
        session = self.get_session()
        async with session.begin():
            query = select(LegoSetsPricesOrm).where(LegoSetsPricesOrm.legoset_id == legoset_id)
            res = await session.execute(query)
            if res:
                legoset_price_orm = res.scalars().first()
                if legoset_price_orm:
                    legoset_price = LegoSetsPrice(
                        legoset_id=legoset_price_orm.legoset_id,
                        price=legoset_price_orm.prices.get(str(website_id), '-'),
                        website_id=website_id,
                        created_at=legoset_price_orm.created_at,
                    )
                    return legoset_price

    @log_decorator(print_args=False)
    async def get_item(self, legoset_id: str) -> LegoSetsPrices | None:
        session = self.get_session()
        async with session.begin():
            query = select(LegoSetsPricesOrm.prices).where(LegoSetsPricesOrm.legoset_id == legoset_id)
            res = await session.execute(query)
            if res:
                legoset_price = res.scalars().first()
                return legoset_price

    @log_decorator(print_args=False, print_kwargs=False)
    async def get_all_items(self) -> list | None:
        session = self.get_session()
        async with session.begin():
            query = select(LegoSetsPricesOrm)
            res = await session.execute(query)
            legosets_prices_orm = res.scalars().all()
            if legosets_prices_orm:
                legosets_prices = [
                    LegoSetsPrices(
                        legoset_id=legoset_price.legoset_id,
                        prices=legoset_price.prices,
                        created_at=legoset_price.created_at
                    ) for legoset_price in legosets_prices_orm]
                return legosets_prices

    @log_decorator(print_args=False, print_kwargs=False)
    async def add_items(self, legosets_prices: LegoSetsPrices):
        session = self.get_session()
        legosets_prices_orm = LegoSetsPricesOrm(
            legoset_id=legosets_prices.legoset_id,
            prices=legosets_prices.prices,
        )
        async with session.begin():
            session.add(legosets_prices_orm)
            await session.commit()

    @log_decorator(print_args=False, print_kwargs=False)
    async def add_item(self, legosets_price: LegoSetsPrice):
        session = self.get_session()
        legosets_prices_orm = LegoSetsPricesOrm(
            legoset_id=legosets_price.legoset_id,
            prices={legosets_price.website_id: legosets_price.price}
        )
        async with session.begin():
            session.add(legosets_prices_orm)
            await session.commit()

    @log_decorator()
    async def delete_price(self, legoset_id: str, website_id: str):
        session = self.get_session()
        async with session.begin():
            query = select(LegoSetsPricesOrm.prices).where(LegoSetsPricesOrm.legoset_id == legoset_id)
            res = await session.execute(query)
            old_prices = res.scalars().first()
            new_prices = {}
            for key in old_prices.keys():
                if key != website_id:
                    new_prices[key] = old_prices[key]
            query = (
                update(LegoSetsPricesOrm)
                .where(LegoSetsPricesOrm.legoset_id == legoset_id)
                .values(prices=new_prices)
            )
            await session.execute(query)
            await session.commit()

if __name__ == '__main__':
    price_repository = LegoSetsPricesRepositoryImpl()


