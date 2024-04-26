import * as TE from 'fp-ts/lib/TaskEither';
import * as Array from 'fp-ts/lib/Array';
import { ObjectStoragePort } from './object-storage.base';
import { PutObjectCommand, S3Client, S3ClientConfig } from '@aws-sdk/client-s3';
import { get } from 'env-var';
import { pipe } from 'fp-ts/lib/function';
import { UploadFile } from 'core/model/file';

export class S3Port implements ObjectStoragePort {
  s3Client: S3Client;
  bucketName: string;
  publicDomain: string;
  constructor() {
    const s3Config: S3ClientConfig = {
      credentials: {
        accessKeyId: get('R2_CLOUDFLARE_ACCESS_KEY').required().asString(),
        secretAccessKey: get('R2_CLOUDFLARE_ACCESS_SECRET')
          .required()
          .asString(),
      },
      endpoint: get('R2_CLOUDFLARE_ENDPOINT').required().asString(),
      region: 'auto',
    };

    const s3Client = new S3Client(s3Config);
    this.s3Client = s3Client;
    this.bucketName = get('R2_BUCKET_NAME').required().asString();
    this.publicDomain = get('R2_PUBLIC').required().asString();
  }
  uploadFiles(files: UploadFile[]): TE.TaskEither<Error, string[]> {
    return pipe(
      files,
      Array.map(({ content, fileName }) =>
        this.uploadSingFile(fileName, content),
      ),
      TE.sequenceArray,
      TE.map((a) => [...a]), // remove readonly for simplicity
    );
  }

  uploadSingFile(
    fileName: string,
    content: Buffer,
  ): TE.TaskEither<Error, string> {
    const bucketParams = {
      Bucket: this.bucketName,
      Key: fileName,
      Body: content,
    };
    return pipe(
      TE.tryCatch(
        async () => this.s3Client.send(new PutObjectCommand(bucketParams)),
        (e) => {
          console.log('upload single fail', e);
          return new Error('UPLOAD_SINGLE_FILE_FAILED');
        },
      ),
      TE.map(() => `${this.publicDomain}/${fileName}`),
    );
  }
}
