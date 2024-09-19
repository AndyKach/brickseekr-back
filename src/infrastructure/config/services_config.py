from application.services.lego_sets_service import LegoSetsService
from infrastructure.config.interfaces_config import lego_parser_interface
from infrastructure.config.repositories_config import lego_sets_repository


def get_lego_sets_service():
    return LegoSetsService(
        lego_sets_repository=lego_sets_repository,
        lego_parser_interface=lego_parser_interface
    )