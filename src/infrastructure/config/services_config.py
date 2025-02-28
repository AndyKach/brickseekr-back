from application.services.legosets_service import LegoSetsService
from application.services.scheduler_service import SchedulerService
from infrastructure.config.interfaces_config import scheduler_interface, search_api_interface
from infrastructure.config.providers_config import websites_interfaces_provider
from infrastructure.config.repositories_config import lego_sets_repository, lego_sets_prices_repository


def get_lego_sets_service():
    return LegoSetsService(
        legosets_repository=lego_sets_repository,
        legosets_prices_repository=lego_sets_prices_repository,
        websites_interfaces_provider=websites_interfaces_provider,
        search_api_interface=search_api_interface,
    )

def get_scheduler_service() -> SchedulerService:
    return SchedulerService(
        scheduler_interface=scheduler_interface,
        lego_sets_service=get_lego_sets_service()
    )
