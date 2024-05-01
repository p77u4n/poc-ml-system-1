import { Statuses, Task, parseTask } from 'core/model/task';
import { BaseCommandService } from 'core/service';
import * as TE from 'fp-ts/lib/TaskEither';
import * as Opt from 'fp-ts/lib/Option';
import * as Either from 'fp-ts/lib/Either';
import { pipe } from 'fp-ts/lib/function';
import { DataSource } from 'typeorm';
import { DMTask } from 'database-typeorm/entities';
import { v1 } from 'uuid';
import { UploadFile } from 'core/model/file';
import { ObjectStoragePort } from 'ports/object-storage.base';
import { TaskQueue } from 'ports/task-queue/task-queue.base';

// has sideeffect so we use IO here to wrap the side-effect logic (FP principle)
const dataMapperForTask = (dmTask: DMTask, task: Task) => () => {
  dmTask.user_id = task.userId;
  dmTask.command = task.command;
  dmTask.status = task.status;
  dmTask.input = JSON.stringify(task.input);
  dmTask.result = pipe(
    task.result,
    Opt.getOrElse(() => null),
  );
  dmTask.id = task.id;
  dmTask.reason = pipe(
    task.failReason,
    Opt.getOrElse(() => null),
  );
  return dmTask;
};

export class TypeORMRabbitMqCMDService implements BaseCommandService {
  constructor(
    private datasource: DataSource,
    private taskQueue: TaskQueue,
    private objectStorageClient: ObjectStoragePort,
  ) {}

  createDMTask = (datasource: DataSource) => (task: Task) => {
    return pipe(
      Either.tryCatch(
        () => {
          return datasource.getRepository(DMTask).create({});
        },
        (e) => new Error(`REQUEST_OTHER_COMMAND_FAILED ${e}`),
      ),
      TE.fromEither,
      TE.chain((dmTask) =>
        // wrap IO of mapping from domain model to data model inside TaskEither
        pipe(dataMapperForTask(dmTask, task), TE.fromIO),
      ),
      TE.chain((dmTask) =>
        TE.tryCatch(
          () => datasource.getRepository(DMTask).save(dmTask),
          () => new Error('SAVE_'),
        ),
      ),
    );
  };
  requestCommand(
    userId: string,
    command: string,
    input: Record<string, any>,
  ): TE.TaskEither<Error, string> {
    return pipe(
      parseTask({
        id: v1(),
        userId,
        command,
        input,
        status: Statuses.PENDING,
      }),
      TE.fromEither,
      TE.tap(this.createDMTask(this.datasource)),
      TE.tap(this.taskQueue.putTask),
      TE.map((task) => task.id),
      // put to rabbimq here
    );
  }
  requestCommandWithFile(
    userId: string,
    command: string,
    files: UploadFile[],
  ): TE.TaskEither<Error, string> {
    return pipe(
      parseTask({
        id: v1(),
        userId,
        command,
        input: {
          fileURIs: [],
        },
        status: Statuses.PENDING,
      }),
      TE.fromEither,
      TE.bindTo('initialTask'),
      TE.bind('uploadFiles', () => this.objectStorageClient.uploadFiles(files)),
      TE.map(({ initialTask, uploadFiles }) => ({
        ...initialTask,
        input: { fileURIs: [...uploadFiles] },
      })),
      TE.tap(this.createDMTask(this.datasource)),
      TE.tap(this.taskQueue.putTask.bind(this.taskQueue)),
      TE.map((task) => task.id),
      // put to rabbimq here
    );
  }
}
