from infrastructure.db.models.legosets_orm import LegoSetsOrm
from application.repositories.legosets_repository import LegoSetsRepository
from domain.legoset import LegoSet
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, text, update

from infrastructure.db.base import async_engine


class LegoSetsRepositoryImpl(LegoSetsRepository):
    def get_session(self) :
        return AsyncSession(bind=async_engine, expire_on_commit=False)

    @staticmethod
    async def orm_to_pydantic(legoset_orm: LegoSetsOrm):
        return LegoSet(
            id=legoset_orm.id,
            name=legoset_orm.name,
            year=legoset_orm.year,
            theme=legoset_orm.theme,
            themeGroup=legoset_orm.themeGroup,
            subtheme=legoset_orm.subtheme,
            images=legoset_orm.images,
            pieces=legoset_orm.pieces,
            dimensions=legoset_orm.dimensions,
            weigh=legoset_orm.weigh,
            tags=legoset_orm.tags,
            description=legoset_orm.description,
            ages_range=legoset_orm.ages_range,
            extendedData=legoset_orm.extendedData,
            launchDate=legoset_orm.launchDate,
            exitDate=legoset_orm.exitDate,
            updated_at=legoset_orm.updated_at,
            created_at=legoset_orm.created_at,
        )

    @staticmethod
    async def pydantic_to_orm(legoset_pydantic: LegoSet):
        return LegoSetsOrm(
            id=legoset_pydantic.id,
            name=legoset_pydantic.name,
            year=legoset_pydantic.year,
            theme=legoset_pydantic.theme,
            themeGroup=legoset_pydantic.themeGroup,
            subtheme=legoset_pydantic.subtheme,
            images=legoset_pydantic.images,
            pieces=legoset_pydantic.pieces,
            dimensions=legoset_pydantic.dimensions,
            weigh=legoset_pydantic.weigh,
            tags=legoset_pydantic.tags,
            description=legoset_pydantic.description,
            ages_range=legoset_pydantic.ages_range,
            extendedData=legoset_pydantic.extendedData,
            launchDate=legoset_pydantic.launchDate,
            exitDate=legoset_pydantic.exitDate,
            updated_at=legoset_pydantic.updated_at,
            created_at=legoset_pydantic.created_at,
        )

    async def get_set(self, set_id: str) -> LegoSet | None:
        session = self.get_session()
        async with session.begin():
            query = (
                select(LegoSetsOrm)
                .where(LegoSetsOrm.id==set_id)
            )
            result = await session.execute(query)
            lego_set_orm = result.scalars().first()

            if lego_set_orm:
                return await self.orm_to_pydantic(legoset_orm=lego_set_orm)
            return None

    async def set_set(self, lego_set: LegoSet):
        session = self.get_session()
        async with session.begin():
            lego_set_orm = await self.pydantic_to_orm(legoset_pydantic=lego_set)
            session.add(lego_set_orm)
            await session.commit()

    async def get_all(self) -> [LegoSet]:
        session = self.get_session()
        async with session.begin():
            query = await session.execute(select(LegoSetsOrm))
            lego_sets_orm = query.scalars().all()
            lego_sets = []
            if lego_sets:
                for lego_set_orm in lego_sets_orm:
                    lego_sets.append(await self.orm_to_pydantic(legoset_orm=lego_set_orm))
            return lego_sets

    async def delete_set(self, lego_set_id):
        session = self.get_session()
        async with session.begin():
            query = delete(LegoSetsOrm).where(LegoSetsOrm.id==lego_set_id)

            await session.execute(query)
            await session.commit()

    async def update_url_name(self, lego_set_id: str, url_name: str):
        session = self.get_session()
        async with session.begin():
            # row = select(LegoSetsOrm).where(LegoSetsOrm.lego_set_id==lego_set_id)
            # print("Befor", row)
            # row.url_name = url_name
            # print("After", row)
            query = update(LegoSetsOrm).where(LegoSetsOrm.id==lego_set_id).values(url_name=url_name)
            await session.execute(query)
            await session.commit()


