import { config } from 'dotenv';
import { get } from 'env-var';
import { DataSource } from 'typeorm';
import * as entities from './entities';

// https://github.com/Sairyss/backend-best-practices#configuration

// Initializing dotenv
config();
// const TYPEORM_PATH_ROOT =
//   __dirname + '/dist/cjs/infrastructure/repository/typeorm';
export const postgresDTsource = new DataSource({
  type: 'postgres',
  host: get('DB_HOST').required().asString(),
  port: get('DB_PORT').required().asIntPositive(),
  username: get('DB_USERNAME').required().asString(),
  password: get('DB_PASSWORD').required().asString(),
  database: get('DB_NAME').required().asString(),
  connectTimeoutMS: 2000,
  logging: ['error', 'migration', 'schema'],
  entities: entities,
  // migrationsTableName: 'migrations',
  // migrations: [TYPEORM_PATH_ROOT + `/migrations/*.js`],
  // seeds: [`${TYPEORM_PATH_ROOT}/seeding/**/*.seeder.ts`],
  // factories: [`${TYPEORM_PATH_ROOT}/factories/**/*.ts`],
});
postgresDTsource
  .initialize()
  .then(() => {
    console.log('Data Source has been initialized!');
  })
  .catch((err) => {
    console.error('Error during Data Source initialization', err);
  });
