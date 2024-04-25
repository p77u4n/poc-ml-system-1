from typing import Any, List, Union

from dino_seedwork_be import tap_excute_future
from returns.functions import tap
from returns.pipeline import pipe

from event_broker_base import DomainEvent, EventBroker


def get_events_list_from_domain_service(
    params: List[Union[Any, List[DomainEvent]]]
) -> List[DomainEvent]:
    return params[1]


def tap_publish_event(event_broker: EventBroker):
    return tap_excute_future(
        pipe(get_events_list_from_domain_service, event_broker.emit_events)
    )
