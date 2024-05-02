from dataclasses import dataclass
from typing import final
from uuid import UUID
from returns.future import FutureResultE, future_safe
from returns.maybe import Maybe
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from infra.sqlalchemy.schema import DMTask
from infra.sqlalchemy.database import engine
from models.task import Task, parse_task
from repository.task import TaskRepository


@final
@dataclass
class PgTaskRepository(TaskRepository):
    session: AsyncSession

    def get_by_id(self, id: UUID) -> FutureResultE[Task]:
        task = future_safe(lambda: self.session.get(DMTask, str(id)))()
        return (
            task.bind(
                lambda t: FutureResultE.from_result(
                    parse_task(
                        id=t.id,
                        command=t.command,
                        status=t.status,
                        raw_input=t.input,
                        result=Maybe.from_optional(t.result),
                        fail_reason=Maybe.from_optional(t.reason),
                    )
                )
            )
            if task is not None
            else FutureResultE.from_failure(Exception("TASK_NOT_EXIST"))
        )

    @future_safe
    async def save(self, task: Task):
        stmt = (
            update(DMTask)
            .where(DMTask.id == str(task.id))
            .values(
                status=task.status.value,
                reason=task.fail_reason.map(lambda r: r.value).value_or(None),
                result=task.result.map(lambda r: r.value).value_or(None),
            )
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        print("result", result)
