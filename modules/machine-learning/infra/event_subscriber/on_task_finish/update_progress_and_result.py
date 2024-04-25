from returns.future import FutureResultE, future_safe
from sqlalchemy import update
from event_broker_base import DomainEvent, SubscriberHandler
from sqlalchemy.orm import Session

from infra.sqlalchemy.schema import Task
from models.task import Status
from models.task_events import get_task_from_event


class UpdateProgressAndResult(SubscriberHandler):
    session: Session

    @future_safe
    async def execute(self, event: DomainEvent):
        task = get_task_from_event(event)
        stmt = (
            update(Task)
            .where(Task.id == task.id)
            .values(
                result=task.result.map(lambda r: r.value).value_or("{}"),
                status=Status.FINISH.value,
            )
        )
        await self.session.execute(stmt)
