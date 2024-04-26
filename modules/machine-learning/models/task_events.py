from enum import Enum


class Events(Enum):
    TASK_FINISH = "TASK_FINISH"
    TASK_FAILED = "TASK_FAILED"
    TASK_START = "TASK_START"
