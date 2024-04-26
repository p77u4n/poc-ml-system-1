from event_broker_base import DomainEvent
from models.task import Task


def get_task_from_event(event: DomainEvent) -> Task:
    return event.props["task"]
