from application.interfaces.scheduler_interface import SchedulerInterface
from application.services.legosets_service import LegosetsService
from domain.job import Job


class SetLegoSchedulerJobsUseCase:
    def __init__(self,
                 scheduler_interface: SchedulerInterface,
                 legosets_service: LegosetsService,
                 ):
        self.scheduler_interface = scheduler_interface
        self.legosets_service = legosets_service

    async def execute(self):
        """
        Функция ставит scheduler работы для парсинга наборов лего
        """
        await self.scheduler_interface.add_job(
            Job(
                func=self.legosets_service.parse_all_legosets_in_store,
                trigger='cron',
                id='lego_parser_store_1',
                day=1,
                hour=2,
                minute=0,
                args=["1"]
            )
        )
        await self.scheduler_interface.add_job(
            Job(
                func=self.legosets_service.parse_all_legosets_in_store,
                trigger='cron',
                id='lego_parser_store_2',
                day=2,
                hour=2,
                minute=0,
                args=["2"]
            )
        )
        await self.scheduler_interface.add_job(
            Job(
                func=self.legosets_service.parse_all_legosets_in_store,
                trigger='cron',
                id='lego_parser_store_3',
                day=3,
                hour=2,
                minute=0,
                args=["3"]
            )
        )
        await self.scheduler_interface.add_job(
            Job(
                func=self.legosets_service.parse_all_legosets_in_store,
                trigger='cron',
                id='lego_parser_store_4',
                day=4,
                hour=2,
                minute=0,
                args=["4"]
            )
        )
        await self.scheduler_interface.add_job(
            Job(
                func=self.legosets_service.parse_all_legosets_in_store,
                trigger='cron',
                id='lego_parser_store_5',
                day=5,
                hour=2,
                minute=0,
                args=["5"]
            )
        )



