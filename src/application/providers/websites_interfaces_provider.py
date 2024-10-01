from abc import ABC, abstractmethod

class WebsitesInterfacesProvider(ABC):
    @abstractmethod
    def get_website_lego_interface(self):
        pass

    @abstractmethod
    def get_website_bricklink_interface(self):
        pass

