from application.interfaces.scheduler_interface import SchedulerInterface
from application.services.legosets_service import LegosetsService
from domain.job import Job


class SetWebsiteLegoSchedulerJobsUseCase:
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
                func=self.legosets_service.tmp_function,
                trigger='cron',
                id='website_lego_parser_1',
                hour=22,
                minute=2,
            )
        )

