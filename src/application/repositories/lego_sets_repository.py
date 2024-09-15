from abc import ABC, abstractmethod

from domain.lego_set import LegoSet


class LegoSetsRepository(ABC):
    @abstractmethod
    def get_set(self, set_id: str) -> LegoSet:
        pass


