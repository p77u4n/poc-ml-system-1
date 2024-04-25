from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic, List, TypeVar

from returns.future import FutureResultE

EventProps = TypeVar("EventProps")


@dataclass
class DomainEvent(Generic[EventProps]):
    tag: str
    props: EventProps


@dataclass
class SubscriberHandler:
    tag: str

    @abstractmethod
    def execute(self, event: DomainEvent) -> FutureResultE:
        pass

    # for distinguishing itself in publisher list of event broker
    def __hash__(self):
        return hash(self.tag)


def get_subscriber_tag(sub: SubscriberHandler):
    return sub.tag


class EventBroker:
    @abstractmethod
    def emit_event(self, event: DomainEvent) -> FutureResultE:
        pass

    @abstractmethod
    def emit_events(self, events: List[DomainEvent]) -> FutureResultE:
        pass

    @abstractmethod
    def subscribe(self, event_tag: str, handler: SubscriberHandler):
        pass
