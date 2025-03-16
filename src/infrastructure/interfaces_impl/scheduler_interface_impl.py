from typing import List

from application.interfaces.scheduler_interface import SchedulerInterface
from domain.job import Job
from infrastructure.config.scheduler_config import scheduler


class SchedulerInterfaceImpl(SchedulerInterface):
    @staticmethod
    async def start() -> None:
        scheduler.start()

    @staticmethod
    async def add_job(job: Job) -> None:
        scheduler.add_job(
            func=job.func,
            trigger=job.trigger,
            day=job.day,
            hour=job.hour,
            minute=job.minute,
            args=job.args,
            id=job.id,
        )

    @staticmethod
    async def delete_job(job_id: str) -> None:
        scheduler.remove_job(job_id)

    @staticmethod
    async def get_all_jobs():
        jobs = scheduler.get_jobs()
        return [f"{job.id} - {job.next_run_time}" for job in jobs]


