from icecream import ic

from application.interfaces.parser_interface import ParserInterface
from application.repositories.lego_sets_repository import LegoSetsRepository


class LegoSetsService:
    def __init__(
            self,
            lego_sets_repository: LegoSetsRepository,
            lego_parser_interface: ParserInterface,
            ):
        self.lego_sets_repository = lego_sets_repository
        self.lego_parser_interface = lego_parser_interface

    async def get_set_info(self, set_id: str):
        return await self.lego_sets_repository.get_set(set_id=set_id)

    async def parse_all_sets(self):
        lego_sets = await self.lego_sets_repository.get_all()
        for lego_set in lego_sets[-50:]:
            ic(lego_set)
            await self.lego_parser_interface.parse_item(item_id=lego_set.lego_set_id)
        # ic(lego_sets)