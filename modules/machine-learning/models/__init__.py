from typing import List, TypeVar, Union

from event_broker_base import DomainEvent

T = TypeVar("T")


def get_domain_service_result(params: List[Union[T, List[DomainEvent]]]) -> T:
    return params[0]
