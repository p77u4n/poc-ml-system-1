from dataclasses import dataclass
from enum import Enum
from returns.maybe import Maybe, Some
from returns.result import Result, ResultE

# from returns.result import ResultE

from models.command import (
    CommandInput,
    CommandType,
    OtherwiseInput,
    PredictInput,
    parse_otherwise_input,
    parse_predict_input_from_json,
)


class Status(Enum):
    FAILED = "FAILED"
    PROCESSING = "PROCESSING"
    FINISH = "FINISH"


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
    command: str,
    status: str,
    fail_reason: Maybe[str],
    result: Maybe[str],
    raw_input: str,
) -> ResultE[Task]:
    match [command, status, fail_reason, result]:
        case [CommandType() as c, Status.PROCESSING, Maybe.empty, Maybe.empty]:
            return parse_input_per_se_command(c, raw_input).map(
                lambda input: Task(
                    c, Status.PROCESSING, Maybe.empty, Maybe.empty, input
                )
            )
        case [CommandType() as c, Status.FAILED, Some(raw_reason), Maybe.empty]:
            return Result.do(
                Task(
                    command=c,
                    status=Status.FAILED,
                    fail_reason=Maybe.from_value(r),
                    result=Maybe.empty,
                    input=input,
                )
                for input in parse_input_per_se_command(c, raw_input)
                for r in parse_reason(raw_reason)
            )
        case [CommandType() as c, Status.FINISH, Maybe.empty, Some(raw_result)]:
            return Result.do(
                Task(
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
            return Result.from_failure(Exception("task is not in correct status"))
