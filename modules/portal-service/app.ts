import { startService } from 'ports/grpc/server';
import { S3Port } from 'ports/s3-storage-port';
import { Registry } from 'registry.base';
import { TypeORMRabbitMqCMDService } from 'service';
import { postgresDTsource } from 'database-typeorm/datasource';
import { runExpress } from 'restapi-view';
import { configDotenv } from 'dotenv';

configDotenv();

const getSingleRegistry = () => {
  const objectStoragePort = new S3Port();
  const commandService = new TypeORMRabbitMqCMDService(
    postgresDTsource,
    objectStoragePort,
  );
  return {
    objectStoragePort,
    commandService,
  };
};

export const registry: Registry = getSingleRegistry();

startService(registry);

runExpress();
