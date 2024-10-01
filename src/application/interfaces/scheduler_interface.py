from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class SchedulerInterface(ABC):
    @staticmethod
    @abstractmethod
    async def start() -> None:
        pass

    @staticmethod
    @abstractmethod
    async def add_job(job) -> None:
        pass

    @staticmethod
    @abstractmethod
    async def delete_job(job_id: str) -> None:
        pass

    @staticmethod
    @abstractmethod
    async def get_all_jobs():
        pass



