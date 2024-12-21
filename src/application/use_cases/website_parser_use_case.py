from abc import ABC, abstractmethod


class WebsiteParserUseCase(ABC):
    @abstractmethod
    def parse_item(self):
        pass

    @abstractmethod
    def parse_items(self):
        pass