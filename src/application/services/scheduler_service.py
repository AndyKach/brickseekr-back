# src/application/services/scheduler_service.py
from datetime import datetime

from application.interfaces.scheduler_interface import SchedulerInterface
from application.services.legosets_service import LegoSetsService
from application.use_cases.set_all_scheduler_jobs_use_case import SetAllSchedulerJobsUseCase
from domain.job import Job

from application.use_cases.set_website_lego_scheduler_jobs_use_case import SetWebsiteLegoSchedulerJobsUseCase


# from application.scheduler.interfaces.scheduler_interface import SchedulerInterface
# from application.scheduler.usecases.set_all_scheduler_use_case import SetAllSchedulersJobsUseCase
# from domain.entities.job import Job


class SchedulerService:
    def __init__(self,
                 scheduler_interface: SchedulerInterface,
                 legosets_service: LegoSetsService
                 ):
        self.scheduler_interface = scheduler_interface

        self.set_website_lego_scheduler_jobs_use_case = SetWebsiteLegoSchedulerJobsUseCase(
            scheduler_interface=scheduler_interface,
            lego_sets_service=legosets_service
        )

        self.set_all_schedulers_jobs = SetAllSchedulerJobsUseCase(
            scheduler_interface=scheduler_interface,
            set_website_lego_scheduler_jobs_use_case=self.set_website_lego_scheduler_jobs_use_case
        )

    async def add_job(self, job: Job) -> None:
        await self.scheduler_interface.add_job(job)

    async def add_all_jobs(self, jobs: list[Job]) -> None:
        for job in jobs:
            await self.scheduler_interface.add_job(job)

    async def delete_job(self, job_id: str) -> None:
        await self.scheduler_interface.delete_job(job_id)

    async def set_all_jobs(self) -> None:
        await self.set_all_schedulers_jobs.execute()

    async def get_all_jobs(self):
        return await self.scheduler_interface.get_all_jobs()

