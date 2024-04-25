from dataclasses import dataclass
from enum import Enum
import uuid
from returns.maybe import Maybe, Some
from returns.result import Result, ResultE, Success, safe
from returns.future import future_safe
import random

# from returns.result import ResultE

from event_broker_base import DomainEvent
from models.command import (
    CommandInput,
    CommandType,
    OtherwiseInput,
    PredictInput,
    parse_command_type,
    parse_otherwise_input,
    parse_predict_input_from_json,
)
from models.task_events import Events


class Status(Enum):
    FAILED = "FAILED"
    PROCESSING = "PROCESSING"
    FINISH = "FINISH"
    PENDING = "PENDING"


@safe
def parse_status(v: str):
    return Status(v)


@dataclass()
class FailReason:
    value: str


def parse_reason(value) -> ResultE[FailReason]:
    return Result.from_value(FailReason(value))


@dataclass()
class RunningResult:
    value: str


def parse_result(value) -> ResultE[RunningResult]:
    return Result.from_value(RunningResult(value))


@dataclass()
class Task:
    id: uuid.UUID
    command: CommandType
    status: Status
    fail_reason: Maybe[FailReason]
    result: Maybe[RunningResult]
    input: PredictInput | OtherwiseInput


def parse_input_per_se_command(
    command: CommandType, input: str
) -> ResultE[CommandInput]:
    match command:
        case CommandType.PREDICT:
            return parse_predict_input_from_json(input)
        case _:
            return parse_otherwise_input(input)


def parse_task(
    id: uuid.UUID,
    command: str,
    status: str,
    fail_reason: Maybe[str],
    result: Maybe[str],
    raw_input: str,
) -> ResultE[Task]:
    domain_command = parse_command_type(command)
    domain_status = parse_status(status)
    match [domain_command, domain_status, fail_reason, result]:
        case [
            Success(c),
            Success(Status.PROCESSING | Status.PENDING),
            Maybe.empty,
            Maybe.empty,
        ]:
            return parse_input_per_se_command(c, raw_input).map(
                lambda input: Task(
                    id, c, domain_status.unwrap(), Maybe.empty, Maybe.empty, input
                )
            )
        case [Success(c), Success(Status.FAILED), Some(raw_reason), Maybe.empty]:
            return Result.do(
                Task(
                    id=id,
                    command=c,
                    status=Status.FAILED,
                    fail_reason=Maybe.from_value(r),
                    result=Maybe.empty,
                    input=input,
                )
                for input in parse_input_per_se_command(c, raw_input)
                for r in parse_reason(raw_reason)
            )
        case [Success(c), Success(Status.FINISH), Maybe.empty, Some(raw_result)]:
            return Result.do(
                Task(
                    id=id,
                    command=c,
                    status=Status.FAILED,
                    fail_reason=Maybe.empty,
                    result=Maybe.from_value(r),
                    input=input,
                )
                for input in parse_input_per_se_command(c, raw_input)
                for r in parse_result(raw_result)
            )
        case _:
            return Result.from_failure(
                Exception(
                    f"task is not in correct status: command-{domain_command}, status={domain_status}, fail_reason={fail_reason}, result={result}"
                )
            )


def clone_task(task: Task):
    return Task(
        id=task.id,
        command=task.command,
        result=task.result,
        fail_reason=task.fail_reason,
        input=task.input,
        status=task.status,
    )


def start_task(task: Task):
    isPending = task.status == Status.PENDING
    if isPending is False:
        return Result.from_failure(Exception("CANNOT_START_A_NON_PENDING_TASK"))
    else:
        updated_task = clone_task(task)
        updated_task.status = Status.PROCESSING
        return Result.from_value(
            [updated_task, [DomainEvent(Events.TASK_START.value, {"task": task})]]
        )


@future_safe
async def running_task(task: Task):
    # machine learning algorithm main process be put at here
    is_failed = bool(random.randint(0, 1))
    updated_task = clone_task(task)
    match is_failed:
        case True:
            updated_task.result = Maybe.from_value(
                parse_result("OK").unwrap()
            )  # panic here
            updated_task.status = Status.FINISH
            return [
                updated_task,
                [DomainEvent(Events.TASK_FINISH.value, {"task": updated_task})],
            ]
        case False:
            updated_task.fail_reason = Maybe.from_value(
                parse_reason("FAILED").unwrap()
            )  # panic here true
            updated_task.status = Status.FAILED
            return [
                updated_task,
                [DomainEvent(Events.TASK_FAILED.value, {"task": updated_task})],
            ]
