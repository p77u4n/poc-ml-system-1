// @ts-nocheck

import * as grpc from 'grpc';
import { packageDefinition } from './server';

const CommandService =
  grpc.loadPackageDefinition(packageDefinition).CommandService;
export const client: grpc.Client = new CommandService(
  'localhost:30043',
  grpc.credentials.createInsecure(),
);
