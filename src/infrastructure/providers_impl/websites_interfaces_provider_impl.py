from application.providers.websites_interfaces_provider import WebsitesInterfacesProvider


class WebsitesInterfacesProviderImpl(WebsitesInterfacesProvider):
    def __init__(self,
                 website_lego_interface,
                 website_bricklink_interface,
                 website_capi_cap_interface,
                 website_museum_of_bricks_interface,
                 website_sparkys_interface,
                 website_kostickyshop_interface,
                 website_brickset_interface,
                 ):
        self.website_lego_interface = website_lego_interface
        self.website_bricklink_interface = website_bricklink_interface
        self.website_capi_cap_interface = website_capi_cap_interface
        self.website_museum_of_bricks_interface = website_museum_of_bricks_interface
        self.website_sparkys_interface = website_sparkys_interface
        self.website_kostickyshop_interface = website_kostickyshop_interface
        self.website_brickset_interface = website_brickset_interface

    def get_website_lego_interface(self):
        return self.website_lego_interface

    def get_website_bricklink_interface(self):
        return self.website_bricklink_interface

    def get_website_capi_cap_interface(self):
        return self.website_capi_cap_interface

    def get_website_museum_of_bricks_interface(self):
        return self.website_museum_of_bricks_interface

    def get_website_sparkys_interface(self):
        return self.website_sparkys_interface

    def get_website_kostickyshop_interface(self):
        return self.website_kostickyshop_interface

    def get_website_brickset_interface(self):
        return self.website_brickset_interface
