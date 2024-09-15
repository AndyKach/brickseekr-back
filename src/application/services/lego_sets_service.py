from application.repositories.lego_sets_repository import LegoSetsRepository


class LegoSetsService:
    def __init__(
            self,
            lego_sets_repository: LegoSetsRepository,
            ):
        self.lego_sets_repository = lego_sets_repository

    async def get_set_info(self, set_id: str):
        return await self.lego_sets_repository.get_set(set_id=set_id)