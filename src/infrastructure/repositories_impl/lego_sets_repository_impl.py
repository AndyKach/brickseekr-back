from src.application.repositories.lego_sets import LegoSetsRepository
from src.domain.lego_set import LegoSet


class LegoSetsRepository(LegoSetsRepository):
    def get_set(self, set_id) -> LegoSet:
        pass