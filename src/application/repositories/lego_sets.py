from abc import ABC, abstractmethod


class LegoSetsRepository(ABC):
    @abstractmethod
    def get_set(self, set_id):
        pass


