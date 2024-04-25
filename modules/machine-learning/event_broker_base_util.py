from typing import Any, List, Union

from returns.functions import tap
from returns.pipeline import flow

from event_broker_base import DomainEvent, EventBroker


def get_events_list_from_domain_service(
    params: List[Union[Any, List[DomainEvent]]]
) -> List[DomainEvent]:
    return params[1]


def tap_publish_event(event_broker: EventBroker):
    return tap(flow(get_events_list_from_domain_service, event_broker.emit_events))
