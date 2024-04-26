from dataclasses import dataclass
from typing import final
from uuid import UUID
from returns.future import FutureResultE
from returns.maybe import Maybe
from returns.pipeline import flow
from sqlalchemy.orm import Session
from infra.sqlalchemy.schema import DMTask
from models.task import Task, parse_task
from repository.task import TaskRepository


@final
@dataclass
class PgTaskRepository(TaskRepository):
    session: Session

    def get_by_id(self, id: UUID) -> FutureResultE[Task]:
        task = self.session.get(DMTask, id)
        return (
            flow(
                parse_task(
                    id=task.id,
                    command=task.command,
                    status=task.status,
                    raw_input=task.input,
                    result=Maybe.from_optional(task.result),
                    fail_reason=Maybe.from_optional(task.reason),
                ),
                FutureResultE.from_result,
            )
            if task is not None
            else FutureResultE.from_failure(Exception("TASK_NOT_EXIST"))
        )
