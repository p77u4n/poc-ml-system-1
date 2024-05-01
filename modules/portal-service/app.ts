import { startService } from 'ports/grpc/server';
import { S3Port } from 'ports/s3-storage-port';
import { TypeORMRabbitMqCMDService } from 'service';
import { postgresDTsource } from 'database-typeorm/datasource';
import { runExpress } from 'restapi-view';
import { configDotenv } from 'dotenv';
import { RabbitTaskQueue } from 'ports/task-queue/rabbit-queue';
import { TE } from 'yl-ddd-ts';
import amqp from 'amqplib';
import { get } from 'env-var';
import { pipe } from 'fp-ts/lib/function';
import * as Either from 'fp-ts/Either';
import { v1 } from 'uuid';

configDotenv();

const getSingleRegistry = () => {
  const objectStoragePort = new S3Port();
  const queueName = 'task-queue';
  const channelCreate = TE.tryCatch(
    () =>
      amqp
        .connect({
          hostname: get('RABBITMQ_HOST').required().asString(),
          username: get('RABBITMQ_POC_USERNAME').required().asString(),
          password: get('RABBITMQ_POC_PWD').required().asString(),
          vhost: get('RABBITMQ_POC_VIRTUAL_HOST').required().asString(),
        })
        .then((c) => c.createChannel())
        .then(async (channel) => {
          channel.assertQueue(queueName, { durable: true });
          return channel;
        }),
    (e) => e as Error,
  );
  return pipe(
    channelCreate,
    TE.map((c) => new RabbitTaskQueue(c, queueName)),
    TE.bindTo('taskQueue'),
    // TE.tap(({ taskQueue }) => taskQueue.putTaskById('testid')),
    TE.bind('objectStoragePort', () => TE.right(objectStoragePort)),
    TE.bind('commandService', ({ taskQueue, objectStoragePort }) =>
      TE.right(
        new TypeORMRabbitMqCMDService(
          postgresDTsource,
          taskQueue,
          objectStoragePort,
        ),
      ),
    ),
  );
};

const start = async () => {
  const registry = await getSingleRegistry()();
  pipe(
    registry,
    Either.match(
      (e) => console.error('REGISTRY_CREATING_FAILED: ', e),
      (reg) => startService(reg),
    ),
  );
  runExpress();
};

start();
