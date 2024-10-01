from application.providers.websites_interfaces_provider import WebsitesInterfacesProvider


class WebsitesInterfacesProviderImpl(WebsitesInterfacesProvider):
    def __init__(self,
                 website_lego_interface,
                 website_bricklink_interface,
                 ):
        self.website_lego_interface = website_lego_interface
        self.website_bricklink_interface = website_bricklink_interface

    def get_website_lego_interface(self):
        return self.website_lego_interface

    def get_website_bricklink_interface(self):
        return self.website_bricklink_interface
