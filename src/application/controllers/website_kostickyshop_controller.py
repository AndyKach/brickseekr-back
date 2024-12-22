from application.interfaces.website_interface import WebsiteInterface
from application.repositories.lego_sets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository


class WebsiteKostikyShopController:
    def __init__(self,
                 lego_sets_repository: LegoSetsRepository,
                 lego_sets_prices_repository: LegoSetsPricesRepository,
                 website_interface: WebsiteInterface,
                 ):
        self.lego_sets_repository = lego_sets_repository,
        self.lego_sets_prices_repository = lego_sets_prices_repository,
        self.website_interface = website_interface