from dataclasses import dataclass
from uuid import UUID

from returns.future import FutureResult
from returns.pipeline import flow

from event_broker_base import EventBroker
from event_broker_base_util import tap_publish_event
from models import get_domain_service_result
from models.task import running_task, start_task
from repository.task import TaskRepository


@dataclass
class TaskUsecases:
    job_repository: TaskRepository
    max_allow_running_jobs: int
    event_broker: EventBroker

    def run_new_task(self, number_of_current_running_jobs: int, task_id: UUID):
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
        is_excess = number_of_current_running_jobs >= self.max_allow_running_jobs
        if is_excess:
            raise Exception("I_AM_OVERLOADED")
        else:
            self.job_repository.get_by_id(task_id).bind(
                flow(start_task, FutureResult.from_result)
            ).bind(tap_publish_event(self.event_broker)).map(
                get_domain_service_result
                # get task from start_task result
            ).bind(
                running_task
            ).bind(
                tap_publish_event(self.event_broker)
            )
