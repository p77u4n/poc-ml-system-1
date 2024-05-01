import { BaseCommandService } from 'core/service';
import { ObjectStoragePort } from 'ports/object-storage.base';
import { TaskQueue } from 'ports/task-queue/task-queue.base';

export interface Registry {
  objectStoragePort: ObjectStoragePort;
  commandService: BaseCommandService;
  taskQueue: TaskQueue;
}
