from application.services.lego_sets_service import LegoSetsService
from infrastructure.config.providers_config import websites_interfaces_provider
from infrastructure.config.repositories_config import lego_sets_repository, lego_sets_prices_repository


def get_lego_sets_service():
    return LegoSetsService(
        lego_sets_repository=lego_sets_repository,
        lego_sets_prices_repository=lego_sets_prices_repository,
        websites_interfaces_provider=websites_interfaces_provider,
    )