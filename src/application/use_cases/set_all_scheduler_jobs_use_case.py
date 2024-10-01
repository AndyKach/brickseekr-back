from application.interfaces.scheduler_interface import SchedulerInterface
from application.use_cases.set_website_lego_scheduler_jobs_use_case import SetWebsiteLegoSchedulerJobsUseCase
from infrastructure.config.logs_config import log_decorator


class SetAllSchedulerJobsUseCase:
    def __init__(self,
                 scheduler_interface: SchedulerInterface,
                 set_website_lego_scheduler_jobs_use_case: SetWebsiteLegoSchedulerJobsUseCase
                 ):
        self.scheduler_interface = scheduler_interface
        self.set_website_lego_scheduler_jobs_use_case = set_website_lego_scheduler_jobs_use_case

    @log_decorator(print_args=False, print_kwargs=False)
    async def execute(self):
        await self.set_website_lego_scheduler_jobs_use_case.execute()

        await self.scheduler_interface.start()
