from unittest.mock import MagicMock, Mock
from uuid import uuid1
import pytest
from returns.functions import tap
from returns.future import FutureResultE
from returns.io import IOFailure, IOSuccess
from returns.maybe import Some
from returns.result import Failure, Success
from config import ServiceConfig
from event_broker_base import EventBroker
from models.task import Events, Status
from repository.task import TaskRepository
from usecase.task import TaskUsecases


@pytest.fixture(scope="function")
def task_use_cases(
    event_broker: EventBroker,
    task_repository: TaskRepository,
    service_config: ServiceConfig,
):
    yield TaskUsecases(
        task_repository=task_repository,
        max_allow_running_jobs=service_config.max_number_of_concurent_job,
        event_broker=event_broker,
    )


async def test_run_new_task(task_use_cases: TaskUsecases, event_broker: EventBroker):
    task_start_sub = Mock()
    task_finish_sub = Mock()
    task_start_sub.execute = MagicMock(
        side_effect=lambda event: FutureResultE.from_value("OK").map(
            tap(lambda _: print("event start", event))
        )
    )
    task_finish_sub.execute = MagicMock(
        side_effect=lambda event: FutureResultE.from_value("OK").map(
            tap(lambda _: print("event finish", event))
        )
    )
    event_broker.subscribe(Events.TASK_START.value, task_start_sub)
    event_broker.subscribe(Events.TASK_FINISH.value, task_finish_sub)
    result = await task_use_cases.run_new_task(2, uuid1()).awaitable()
    match result:
        case IOSuccess(Success(task)):
            assert task.status == Status.FINISH
            match task.result:
                case Some(r):
                    assert r.value == "OK"
                case _:
                    assert False
            task_start_sub.execute.assert_called_once()
            task_finish_sub.execute.assert_called_once()
        case IOFailure(Failure(e)):
            print("exception ", e)
            assert False


async def test_overload_prevent(
    task_use_cases: TaskUsecases, service_config: ServiceConfig
):
    result = await task_use_cases.run_new_task(
        service_config.max_number_of_concurent_job, uuid1()
    ).awaitable()

    match result:
        case IOFailure(Failure()):
            assert True
        case IOSuccess(Success()):
            assert False
