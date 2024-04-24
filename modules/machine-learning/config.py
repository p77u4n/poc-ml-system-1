from dataclasses import dataclass
from dino_seedwork_be import get_env


@dataclass
class ServiceConfig:
    max_number_of_concurent_job: int


env_service_config = ServiceConfig(
    max_number_of_concurent_job=int(get_env("MAX_NUMBER_JOBS") or 1)
)
