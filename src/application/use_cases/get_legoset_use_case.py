from application.repositories.lego_sets_repository import LegoSetsRepository
from domain.legoset import LegoSet


class GetLegoSetUseCase:
    def __init__(self,
                 legosets_repository: LegoSetsRepository
                 ):
        self.legosets_repository = legosets_repository

    async def execute(self, legoset_id: str):
        legoset = await self.legosets_repository.get_set(set_id=legoset_id)
        legoset = await self.validate_datetime_values(legoset)
        return legoset

    @staticmethod
    async def validate_datetime_values(legoset: LegoSet):
        if legoset.launchDate:
            legoset.launchDate = legoset.launchDate.isoformat()
        if legoset.exitDate:
            legoset.exitDate = legoset.exitDate.isoformat()
        if legoset.updated_at:
            legoset.updated_at = legoset.updated_at.isoformat()
        if legoset.created_at:
            legoset.created_at = legoset.created_at.isoformat()
        return legoset
