import { BaseCommandService } from 'core/service';
import { ObjectStoragePort } from 'ports/object-storage.base';

export interface Registry {
  objectStoragePort: ObjectStoragePort;
  commandService: BaseCommandService;
}
