import * as TE from 'fp-ts/TaskEither';
import { Task } from '../model/task';
import { UploadFile } from 'core/model/file';

export interface BaseQueryService {
  getMyTasks(userId: string): TE.TaskEither<Error, Task[]>;
  getMyTaskById(userId: string, taskId: string): TE.TaskEither<Error, Task>;
}

export interface BaseCommandService {
  requestCommand(
    userId: string,
    command: string,
    input: Record<string, any>,
  ): TE.TaskEither<Error, string>;

  requestCommandWithFile(
    userId: string,
    command: string,
    files: UploadFile[],
  ): TE.TaskEither<Error, string>;
}
