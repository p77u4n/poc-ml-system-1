from returns.future import future_safe
from sqlalchemy import update
from event_broker_base import DomainEvent, SubscriberHandler
from sqlalchemy.orm import Session

from infra.sqlalchemy.schema import Task
from models.task import Status
from models.task_events import get_task_from_event


class UpdateFailedProgressAndLog(SubscriberHandler):
    session: Session

    @future_safe
    async def execute(self, event: DomainEvent):
        # at here we can have some additional side-effect
        # like push email notification to user, or push a failure event to telemetry
        task = get_task_from_event(event)
        stmt = (
            update(Task)
            .where(Task.id == task.id)
            .values(
                status=Status.FAILED.value,
                reason=task.fail_reason.map(lambda r: r.value).value_or(""),
            )
        )
        await self.session.execute(stmt)
