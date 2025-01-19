from abc import ABC, abstractmethod

class WebsitesInterfacesProvider(ABC):
    @abstractmethod
    def get_website_lego_interface(self):
        pass

    @abstractmethod
    def get_website_bricklink_interface(self):
        pass

    @abstractmethod
    def get_website_museum_of_bricks_interface(self):
        pass

    @abstractmethod
    def get_website_capi_cap_interface(self):
        pass

    @abstractmethod
    def get_website_sparkys_interface(self):
        pass

    @abstractmethod
    def get_website_kostickyshop_interface(self):
        pass

    @abstractmethod
    def get_website_brickset_interface(self):
        pass








