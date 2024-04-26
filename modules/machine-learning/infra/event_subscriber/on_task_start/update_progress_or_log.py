from returns.future import future_safe
from sqlalchemy import update
from event_broker_base import DomainEvent, SubscriberHandler
from sqlalchemy.orm import Session

from infra.sqlalchemy.schema import DMTask
from models.task import Status
from models.task_events_utils import get_task_from_event


class UpdateStartProgressAndLog(SubscriberHandler):
    session: Session

    @future_safe
    async def execute(self, event: DomainEvent):
        # at here we can have some additional side-effect
        # like push email notification to user, or push a start event to telemetry
        task = get_task_from_event(event)
        stmt = (
            update(DMTask)
            .where(DMTask.id == task.id)
            .values(
                status=Status.PROCESSING.value,
            )
        )
        await self.session.execute(stmt)
