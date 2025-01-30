from application.controllers.website_brickset_controller import WebsiteBricksetController
from application.repositories.legosets_repository import LegoSetsRepository
from domain.legoset import LegoSet


class GetLegoSetUseCase:
    def __init__(self,
                 legosets_repository: LegoSetsRepository,
                 website_brickset_controller: WebsiteBricksetController

                 ):
        self.legosets_repository = legosets_repository
        # self.website_lego_parser_use_case = website_lego_parser_use_case
        self.website_brickset_controller = website_brickset_controller

    async def execute(self, legoset_id: str):
        legoset = await self.legosets_repository.get_set(set_id=legoset_id)
        if legoset:
            legoset = await self.validate_datetime_values(legoset)
        else:
            pass
            # TODO 1. спарсить, сохранить, вернуть
            # await self.website_brickset_parser_use_case.parse
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
