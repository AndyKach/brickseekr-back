import logging
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, text, update

from infrastructure.db.base import async_engine

from application.repositories.websites_repository import WebsitesRepository
from domain.website import Website
from infrastructure.db.models.websites_orm import WebsitesOrm

system_logger = logging.getLogger("system_logger")

class WebsitesRepositoryImpl(WebsitesRepository):
    def get_session(self) :
        return AsyncSession(bind=async_engine, expire_on_commit=False)

    def orm_to_pydantic(self, website_orm: WebsitesOrm):
        return Website(
            id=website_orm.id,
            name=website_orm.name,
            link=website_orm.link,
            created_at=website_orm.created_at
        )

    async def get_website_info(self, website_id: str) -> Website:
        session = self.get_session()
        async with session.begin():
            query = (
                select(WebsitesOrm)
                .where(WebsitesOrm.id==int(website_id))
            )
            result = await session.execute(query)
            website_orm = result.scalars().first()
            if website_orm:
                return self.orm_to_pydantic(website_orm)
            return None