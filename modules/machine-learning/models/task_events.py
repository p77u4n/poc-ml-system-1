from enum import Enum

from event_broker_base import DomainEvent
from models.task import Task


class Events(Enum):
    TASK_FINISH = "TASK_FINISH"
    TASK_FAILED = "TASK_FAILED"
    TASK_START = "TASK_START"


def get_task_from_event(event: DomainEvent) -> Task:
    return event.props["task"]
