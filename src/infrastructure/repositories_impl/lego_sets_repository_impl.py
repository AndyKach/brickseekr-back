from infrastructure.db.models.legosets_orm import LegoSetsOrm
from application.repositories.lego_sets_repository import LegoSetsRepository
from domain.lego_set import LegoSet
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, text, update

from infrastructure.db.base import async_engine


class LegoSetsRepositoryImpl(LegoSetsRepository):
    def get_session(self) :
        return AsyncSession(bind=async_engine, expire_on_commit=False)

    async def get_set(self, set_id: str) -> LegoSet | None:
        session = self.get_session()
        async with session.begin():
            query = (
                select(LegoSetsOrm)
                .where(LegoSetsOrm.lego_set_id==set_id)
            )
            result = await session.execute(query)
            lego_set = result.scalars().first()
            if lego_set:
                return LegoSet(
                    lego_set_id=lego_set.lego_set_id,
                    images=lego_set.images,
                    name=lego_set.name,
                    category_name=lego_set.category_name,
                    url_name=lego_set.url_name,
                    year=lego_set.year,
                    weigh=lego_set.weigh,
                    dimensions=lego_set.dimensions,
                    ages=lego_set.ages,
                    created_at=lego_set.created_at.isoformat(),
                )
            return None

    async def set_set(self, lego_set: LegoSet):
        session = self.get_session()
        async with session.begin():
            lego_set_orm = LegoSetsOrm(
                lego_set_id=lego_set.lego_set_id,
                images=lego_set.images,
                name=lego_set.name,
                category_name=lego_set.category_name,
                url_name=lego_set.url_name,
                year=lego_set.year,
                weigh=lego_set.weigh,
                dimensions=lego_set.dimensions,
                ages=lego_set.ages,
                created_at=lego_set.created_at,
            )
            session.add(lego_set_orm)
            await session.commit()

    async def get_all(self) -> [LegoSet]:
        session = self.get_session()
        async with session.begin():
            query = await session.execute(select(LegoSetsOrm))
            lego_sets_orm = query.scalars().all()
            lego_sets = []
            if lego_sets:
                for lego_set in lego_sets_orm:
                    lego_sets.append(LegoSet(
                        lego_set_id=lego_set.lego_set_id,
                        images=lego_set.images,
                        name=lego_set.name,
                        category_name=lego_set.category_name,
                        url_name=lego_set.url_name,
                        year=lego_set.year,
                        weigh=lego_set.weigh,
                        dimensions=lego_set.dimensions,
                        ages=lego_set.ages,
                        created_at=lego_set.created_at,
                    ))
            return lego_sets

    async def delete_set(self, lego_set_id):
        session = self.get_session()
        async with session.begin():
            query = delete(LegoSetsOrm).where(LegoSetsOrm.lego_set_id==lego_set_id)

            await session.execute(query)
            await session.commit()

    async def update_url_name(self, lego_set_id: str, url_name: str):
        session = self.get_session()
        async with session.begin():
            # row = select(LegoSetsOrm).where(LegoSetsOrm.lego_set_id==lego_set_id)
            # print("Befor", row)
            # row.url_name = url_name
            # print("After", row)
            query = update(LegoSetsOrm).where(LegoSetsOrm.lego_set_id==lego_set_id).values(url_name=url_name)
            await session.execute(query)
            await session.commit()


