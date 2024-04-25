from typing import Any, List, Union

from event_broker_base import DomainEvent


def get_domain_service_result[T](params: List[Union[T, List[DomainEvent]]]) -> T:
    return params[0] 
