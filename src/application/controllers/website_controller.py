from abc import ABC, abstractmethod

class WebsiteController(ABC):
    @abstractmethod
    def parse_lego_sets(self):
        pass