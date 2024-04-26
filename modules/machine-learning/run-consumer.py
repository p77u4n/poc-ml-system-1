import os
import sys

from infra.sqlalchemy.database import SessionLocal

sys.path.append(os.getcwd())

from uuid import UUID
from dino_seedwork_be import get_env
import jsonpickle
import pika
import time

from returns.io import IOSuccess
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import count

from event_broker_in_memory import EventBrokerInMemory
from models.task import Status
from usecase.task import TaskUsecases
from config import env_service_config
from infra.repo.pg_task import PgTaskRepository
from infra.sqlalchemy.schema import DMTask

username = str(get_env("RABBITMQ_POC_USERNAME") or "username")
pwd = str(get_env("RABBITMQ_POC_PWD") or "pwd")


def run_consumer(session: Session):
    host = str(get_env("RABBITMQ_HOST") or "/")
    virtual_host = str(get_env("RABBITMQ_POC_VIRTUAL_HOST") or "/")
    credentials = pika.PlainCredentials(username, pwd)
    print(f"pika: ${host}, ${virtual_host}")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=host,
            virtual_host=virtual_host,
            credentials=credentials,
        )
    )
    channel = connection.channel()
    task_repo = PgTaskRepository(session)
    event_broker = EventBrokerInMemory()
    task_service = TaskUsecases(
        task_repo, env_service_config.max_number_of_concurent_job, event_broker
    )
    channel.queue_declare(queue="task_queue", durable=True)
    print(" [*] Waiting for messages. To exit press CTRL+C")

    async def callback(ch, method, properties, body):
        stmt = select(count(DMTask.id)).where(DMTask.status == Status.PROCESSING.value)
        count_current_job = (await session.execute(stmt)).scalars().one()
        result = await task_service.run_new_task(
            count_current_job, UUID(jsonpickle.decode(body.decode())["taskId"])
        )
        print(f" [x] Received {body.decode()}")
        match result:
            case IOSuccess():
                ch.basic_ack(delivery_tag=method.delivery_tag)
                print(" [x] Done")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="task_queue", on_message_callback=callback)

    channel.start_consuming()


run_consumer(SessionLocal())
