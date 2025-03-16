from application.repositories.websites_repository import WebsitesRepository
from domain.website import Website


class GetWebsiteUseCase:
    def __init__(self,
                 websites_repository: WebsitesRepository,
                 ):
        self.websites_repository = websites_repository

    async def get_website(self, website_id: str) -> Website:
        """
        Функция возвращает данные о вебсайте
        """
        return await self.websites_repository.get_website_info(website_id=website_id)
