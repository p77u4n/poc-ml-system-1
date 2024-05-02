from asyncio import sleep
from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from dino_seedwork_be import tap_excute_future
from returns.functions import tap
from returns.future import FutureResult, FutureResultE, future_safe
from returns.pipeline import flow, pipe

from config import ServiceConfig
from event_broker_base import EventBroker
from event_broker_base_util import tap_publish_event
from models import get_domain_service_result
from models.task import Status, Task, running_task, start_task
from repository.task import TaskRepository


class TaskUsecaseExceptions(Enum):
    task_already_run = "TASK_ALREADY_RUN"
    overloaded = "I_AM_OVERLOADED"


@dataclass
class TaskUsecases:
    task_repository: TaskRepository
    max_allow_running_jobs: int
    event_broker: EventBroker
    config: ServiceConfig

    def run_new_task(
        self, number_of_current_running_jobs: int, task_id: UUID
    ) -> FutureResultE[Task]:
        print("delay in ", self.config.max_mocking_process_delay_minutes)
        # in an usecase of application layer, we need transactional consistency
        # for example in this usecase
        #   * we need assure the task would be runned immediately without interfered
        #     by any oulier factor, and the result would be updated right after it finish
        #   * but we also want some side effect (mostly for interface logic like displaying
        #     the task progress status to user, and they are not too important to integrate
        #     the logic of user layer, so) that can be happen in eventually consistency manner
        #     with the main logic (the above logic) -> using event driven pattern, so we can make
        #     our usecase logic pluginable (open for extension) with some supporting side-effect like
        #     logging, or status updating. This event driven pattern also helps us decouple the availabilty
        #     -coupling between db infrastructure and the machine-learning service

        def validate_task_for_running(task: Task):
            is_excess = number_of_current_running_jobs >= self.max_allow_running_jobs
            match [task.status, is_excess]:
                case [Status.PENDING, False]:
                    return FutureResultE.from_value(task)
                case [Status.PENDING, True]:
                    return FutureResultE.from_failure(
                        Exception(TaskUsecaseExceptions.overloaded)
                    )
                case _:
                    return FutureResultE.from_failure(
                        Exception(TaskUsecaseExceptions.task_already_run)
                    )

        return (
            self.task_repository.get_by_id(task_id)
            .bind(validate_task_for_running)
            .bind(pipe(start_task, FutureResult.from_result))
            .bind(
                tap_excute_future(
                    pipe(get_domain_service_result, self.task_repository.save)
                )
            )
            .bind(tap_publish_event(self.event_broker))
            .map(
                get_domain_service_result
                # get task from start_task result
            )
            .bind(running_task)
            .bind(
                tap_excute_future(
                    # fake a time that consumed by machine learning algorithm running
                    future_safe(
                        lambda _: sleep(
                            self.config.max_mocking_process_delay_minutes * 60
                        )
                    )
                )
            )
            .bind(tap_publish_event(self.event_broker))
            .map(
                get_domain_service_result
                # get task from running_task result
            )
            .bind(tap_excute_future(self.task_repository.save))
        )
