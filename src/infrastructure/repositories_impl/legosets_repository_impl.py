import logging

from icecream import ic
from sqlalchemy.orm.attributes import flag_modified

from infrastructure.db.models.legosets_orm import LegoSetsOrm
from application.repositories.legosets_repository import LegoSetsRepository
from domain.legoset import LegoSet
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, text, update

from infrastructure.db.base import async_engine

system_logger = logging.getLogger("system_logger")

class LegoSetsRepositoryImpl(LegoSetsRepository):
    def get_session(self) :
        return AsyncSession(bind=async_engine, expire_on_commit=False)

    @staticmethod
    async def orm_to_pydantic(legoset_orm: LegoSetsOrm):
        return LegoSet(
            id=legoset_orm.id,
            name=legoset_orm.name,
            year=legoset_orm.year,
            rating=legoset_orm.rating,
            google_rating=legoset_orm.google_rating,
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
            minifigures_count=legoset_orm.minifigures_count,
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
            rating=legoset_pydantic.rating,
            google_rating=legoset_pydantic.google_rating,
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
            minifigures_count=legoset_pydantic.minifigures_count,
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
            legoset_orm = result.scalars().first()

            if legoset_orm:
                return await self.orm_to_pydantic(legoset_orm=legoset_orm)
            return None

    async def set_set(self, legoset: LegoSet):
        session = self.get_session()
        async with session.begin():
            legoset_orm = await self.pydantic_to_orm(legoset_pydantic=legoset)
            session.add(legoset_orm)
            await session.commit()

    async def get_all(self) -> [LegoSet]:
        session = self.get_session()
        async with session.begin():
            query = await session.execute(select(LegoSetsOrm))
            legosets_orm = query.scalars().all()
            # print(legosets_orm)
            legosets = []
            if legosets_orm:
                for legoset_orm in legosets_orm:
                    legosets.append(await self.orm_to_pydantic(legoset_orm=legoset_orm))
                return legosets

    async def get_top_rating(self, legosets_count: int):
        session = self.get_session()
        async with session.begin():
            query = await session.execute(
                select(LegoSetsOrm).filter(LegoSetsOrm.rating.isnot(None)).order_by(LegoSetsOrm.rating.desc()).limit(legosets_count)
            )
            legosets_orm = query.scalars().all()
            # print(legosets_orm)
            legosets = []
            if legosets_orm:
                for legoset_orm in legosets_orm:
                    legosets.append(await self.orm_to_pydantic(legoset_orm=legoset_orm))
                return legosets


    async def delete_set(self, legoset_id):
        session = self.get_session()
        async with session.begin():
            query = delete(LegoSetsOrm).where(LegoSetsOrm.id == legoset_id)

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


    async def update_set(self, legoset: LegoSet) -> None:
        session = self.get_session()
        async with session.begin():
            query = select(LegoSetsOrm).where(LegoSetsOrm.id==legoset.id)
            result = await session.execute(query)
            legoset_orm = result.scalars().first()

            # system_logger.info(legoset_orm)
            # system_logger.info(legoset.model_fields)
            # system_logger.info(legoset.model_fields.items())

            for key in legoset.model_dump():
                # system_logger.info(f"Key: {key}, Value: {getattr(legoset, key)}")
                # system_logger.info(f"Key: {key}, Value: ")
                if getattr(legoset_orm, key) != getattr(legoset, key):
                    if getattr(legoset, key) != 0 and \
                        getattr(legoset, key) is not None and \
                            getattr(legoset, key) != {} and \
                                getattr(legoset, key) != [] and \
                                    getattr(legoset, key) != 0.0 and \
                                        getattr(legoset, key) != "":
                                            setattr(legoset_orm, key, getattr(legoset, key))
                                            flag_modified(legoset_orm, key)

    async def update_rating(self, legoset_id: str, rating: float):
        session = self.get_session()
        async with session.begin():
            query = update(LegoSetsOrm).where(LegoSetsOrm.id==legoset_id).values(rating=rating)
            await session.execute(query)
            await session.commit()

    async def update_google_rating(self, legoset_id: str, google_rating: float):
        session = self.get_session()
        async with session.begin():
            query = update(LegoSetsOrm).where(LegoSetsOrm.id==legoset_id).values(google_rating=google_rating)
            await session.execute(query)
            await session.commit()

    async def update_images(self, legoset_id: str, images: dict):
        session = self.get_session()
        async with session.begin():
            query = (
                select(LegoSetsOrm.images)
                .where(LegoSetsOrm.id == legoset_id)
            )
            res = await session.execute(query)
            new_images = res.scalars().first()
            # ic(f"IMAGES LEGOSET({legoset_id}) BEFORE: {new_images}")
            for image in images.keys():
                new_images[image] = images[image]

            # ic(f"IMAGES LEGOSET({legoset_id}) AFTER: {new_images}")

            query = (
                update(LegoSetsOrm)
                .where(LegoSetsOrm.id == legoset_id)
                .values(images=new_images)
            )
            await session.execute(query)
            await session.commit()

    async def update_extended_data(self, legoset_id: str, extended_data: dict) -> None:
        """
        extended_data: {"cz_url_name": str, "cz_category_name": str}
        """
        session = self.get_session()
        async with session.begin():
            query = (
                select(LegoSetsOrm.extendedData)
                .where(LegoSetsOrm.id == legoset_id)
            )
            res = await session.execute(query)
            data = res.scalars().first()
            system_logger.info(f"extended_data: {extended_data}")
            system_logger.info(f"data before: {data}")
            data['cz_url_name'] = extended_data['cz_url_name']
            data['cz_category_name'] = extended_data['cz_category_name']
            system_logger.info(f"data after: {data}")
            query = (
                update(LegoSetsOrm)
                .where(LegoSetsOrm.id == legoset_id)
                .values(extendedData=data)
            )
            await session.execute(query)
            await session.commit()



