from abc import ABC, abstractmethod

class WebsiteDataSourceInterface(ABC):
    @abstractmethod
    def parse_all_legosets(self):
        pass
