from application.interfaces.scheduler_interface import SchedulerInterface
from application.services.lego_sets_service import LegoSetsService
from domain.job import Job


class SetWebsiteLegoSchedulerJobsUseCase:
    def __init__(self,
                 scheduler_interface: SchedulerInterface,
                 lego_sets_service: LegoSetsService,
                 ):
        self.scheduler_interface = scheduler_interface
        self.lego_sets_service = lego_sets_service

    async def execute(self):
        await self.scheduler_interface.add_job(
            Job(
                func=self.lego_sets_service.tmp_function,
                trigger='cron',
                id='website_lego_parser_1',
                hour=22,
                minute=2,
            )
        )

