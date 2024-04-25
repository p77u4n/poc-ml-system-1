from abc import ABC, abstractmethod
from uuid import UUID

from returns.future import FutureResult, FutureResultE

from models.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: UUID) -> FutureResultE[Task]:
        pass
