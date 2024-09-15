from application.services.lego_sets_service import LegoSetsService
from infrastructure.config.repositories_config import lego_sets_repository


def get_lego_sets_service():
    return LegoSetsService(
        lego_sets_repository=lego_sets_repository
    )