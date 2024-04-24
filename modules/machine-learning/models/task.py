from dataclasses import dataclass
from enum import Enum
from returns.maybe import Maybe

# from returns.result import ResultE

from models.command import CommandType


class Status(Enum):
    FAILED = "FAILED"
    PROCESSING = "PROCESSING"
    FINISH = "FINISH"


@dataclass()
class Task:
    command: CommandType
    status: Status
    fail_reason: Maybe[str]
    result: Maybe[str]


# def parse_task(
#     command: string, status: string, fail_reason: Maybe[str], result: Maybe[str]
# ) -> ResultE[Task]:
#     match [status, fail_reason, result]:
#         case [CommandType.PREDICT, Maybe.empty, Maybe.empty]:
#             pass
