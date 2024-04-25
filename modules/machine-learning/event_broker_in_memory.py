from typing import Dict, List, Set, final
from dino_seedwork_be import collect_fresult, collect_result
from returns.future import FutureResult, FutureResultE
from returns.iterables import Fold
from event_broker_base import DomainEvent, EventBroker, SubscriberHandler


@final
class EventBrokerInMemory(EventBroker):
    subscribers: Dict[str, Set[SubscriberHandler]]

    def __init__(self) -> None:
        self.subscribers = {}
        super().__init__()

    def _get_list_subs(self, event_tag: str) -> Set[SubscriberHandler]:
        return self.subscribers[event_tag] if event_tag in self.subscribers else set()

    def emit_event(self, event: DomainEvent):
        subs = self._get_list_subs(event.tag)
        return collect_fresult(
            [sub.execute(event) for sub in subs], FutureResult.from_value(())
        )

    def emit_events(self, events: List[DomainEvent]):
        return collect_fresult(
            [self.emit_event(event) for event in events], FutureResult.from_value(())
        )

    def subscribe(self, event_tag: str, handler: SubscriberHandler):
        subs = self._get_list_subs(event_tag)
        self.subscribers[event_tag] = {handler} | subs
