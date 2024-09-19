from infrastructure.db.models.lego_sets_orm import LegoSetsOrm
from application.repositories.lego_sets_repository import LegoSetsRepository
from domain.lego_set import LegoSet
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, text

from infrastructure.db.base import async_engine


class LegoSetsRepositoryImpl(LegoSetsRepository):
    def get_session(self) :
        return AsyncSession(bind=async_engine, expire_on_commit=False)

    async def get_set(self, set_id: str) -> LegoSet:
        session = self.get_session()
        async with session.begin():
            query = (
                select(LegoSetsOrm)
                .where(LegoSetsOrm.lego_set_id==set_id)
            )
            result = await session.execute(query)
            lego_set = result.scalars().first()

            if lego_set is None:
                return "Set is not exist"

            return LegoSet(
                lego_set_id=lego_set.lego_set_id,
                images=lego_set.images,
                name=lego_set.name,
                year=lego_set.year,
                weigh=lego_set.weigh,
                dimensions=lego_set.dimensions,
                ages=lego_set.ages,
                created_at=lego_set.created_at,
            )

    async def set_set(self, lego_set: LegoSet):
        session = self.get_session()
        async with session.begin():
            lego_set_orm = LegoSetsOrm(
                lego_set_id=lego_set.lego_set_id,
                images=lego_set.images,
                name=lego_set.name,
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
            for lego_set in lego_sets_orm:
                lego_sets.append(LegoSet(
                    lego_set_id=lego_set.lego_set_id,
                    images=lego_set.images,
                    name=lego_set.name,
                    year=lego_set.year,
                    weigh=lego_set.weigh,
                    dimensions=lego_set.dimensions,
                    ages=lego_set.ages,
                    created_at=lego_set.created_at,
                ))
            return lego_sets

