import * as TE from 'fp-ts/TaskEither';

export interface ObjectStoragePort {
  uploadFiles(
    files: { content: Buffer; fileName: string }[],
  ): TE.TaskEither<Error, string[]>;
}
