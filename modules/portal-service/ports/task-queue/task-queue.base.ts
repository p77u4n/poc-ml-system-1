import { Task } from 'core/model/task';
import * as TE from 'fp-ts/lib/TaskEither';

export interface TaskQueue {
  putTask(task: Task): TE.TaskEither<Error, void>;
  putTaskById(id: string): TE.TaskEither<Error, void>;
}
