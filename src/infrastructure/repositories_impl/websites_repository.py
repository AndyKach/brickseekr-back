from abc import ABC, abstractmethod

from domain.website import Website


class WebsitesRepository(ABC):
    @abstractmethod
    def get_website_info(self, website_id: str) -> Website:
        pass