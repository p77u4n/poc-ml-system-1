from dataclasses import dataclass
from dino_seedwork_be import get_env


@dataclass
class ServiceConfig:
    max_number_of_concurent_job: int
    max_mocking_process_delay_minutes: float


env_service_config = ServiceConfig(
    max_number_of_concurent_job=int(get_env("MAX_NUMBER_JOBS") or 1),
    max_mocking_process_delay_minutes=float(
        get_env("MAX_MOCKING_PROCESS_DELAY") or 0.2
    ),
)
