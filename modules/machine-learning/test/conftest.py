from uuid import UUID
import jsonpickle
import jsonpickle
import pytest
from returns.future import Future, FutureResult
from returns.maybe import Maybe

from config import ServiceConfig
from event_broker_in_memory import EventBrokerInMemory
from models.command import CommandType
from models.task import Status, parse_task
from repository.task import TaskRepository
from unittest.mock import MagicMock


@pytest.fixture()
def event_broker():
    yield EventBrokerInMemory()


@pytest.fixture()
def service_config():
    yield ServiceConfig(3, 5)


class MockTaskRepository(TaskRepository):
    def get_by_id(self, id: UUID):
        return FutureResult.from_failure(Exception("NOT_IMPLEMENT_YET"))


@pytest.fixture()
def task_repository():
    mock_repo = MockTaskRepository()
    mock_repo.get_by_id = MagicMock(
        side_effect=lambda id: FutureResult.from_result(
            parse_task(
                id=id,
                command=CommandType.PREDICT.value,
                status=Status.PENDING.value,
                raw_input=str(
                    jsonpickle.encode(
                        {
                            "top_left_x": 1.1,
                            "top_left_y": 1.1,
                            "bottom_right_x": 2.2,
                            "bottom_right_y": 2.2,
                        }
                    )
                ),
                fail_reason=Maybe.empty,
                result=Maybe.empty,
            )
        )
    )
    yield mock_repo
