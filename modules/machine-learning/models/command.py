from dataclasses import dataclass
from enum import Enum

from dino_seedwork_be import feed_identity
from jsonpickle import json
from returns.result import Result, ResultE, safe


class CommandType(Enum):
    PREDICT = "PREDICT"
    EXPORT = "EXPORT"
    LOGS = "LOGS"
    DATASET_CREATE = "DATASET_CREATE"
    DOWNLOAD = "DOWNLOAD"


### FILE input value object
@dataclass()
class FileInput:
    file_url: str


### PREDICT_INPUT value object
@dataclass()
class Point:
    x: float
    y: float


def parse_point(x: float, y: float) -> ResultE[Point]:
    return Result.from_value(Point(x, y))


@dataclass()
class PredictInput:
    top_left: Point
    bottom_right: Point


### Other kind of input value object
## that for LOGS, DATASET_CREATE, DOWNLOAD
## i stipulate that they includes file uploaded
@dataclass()
class OtherwiseInput(FileInput):
    pass


def parse_predict_input_from_json(json_str: str) -> ResultE[PredictInput]:
    # logic parse predict_input valueobject from json
    @safe
    def parse_raw_rect_coord_from_json(json_str: str):
        vjson = json.decode(json_str) or {}
        # This kind of below mapping may seem absurd or ridiculous,
        # but I do this to only check if the object we get from JSON
        # has enough data we need. If it doesn't, the KeyError will be returned and
        # caught by the safe decorator, safely wrapped in a Result monad.
        return {
            "top_left_x": vjson["top_left_x"],
            "top_left_y": vjson["top_left_y"],
            "bottom_right_x": vjson["bottom_right_x"],
            "bottom_right_y": vjson["bottom_right_y"],
        }

    return (
        parse_raw_rect_coord_from_json(json_str)
        .bind(
            lambda params: Result.do(
                {"top_left": top_left, "bottom_right": bottom_right}
                for top_left in parse_point(params["top_left_x"], params["top_left_y"])
                for bottom_right in parse_point(
                    params["bottom_right_x"], params["bottom_right_y"]
                )
            )
        )
        .map(lambda params: PredictInput(params["top_left"], params["bottom_right"]))
        .alt(feed_identity(Exception("CANNOT_PARSE_COORD")))
    )


def parse_otherwise_input(json_str: str) -> ResultE[OtherwiseInput]:
    @safe
    def parse_file_from_json(json_str: str):
        vjson = json.decode(json_str) or {}
        return vjson["file_url"]

    return parse_file_from_json(json_str).map(OtherwiseInput)
