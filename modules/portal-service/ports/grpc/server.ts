// @ts-nocheck
import * as grpc from 'grpc';
import * as protoLoader from '@grpc/proto-loader';
import { v1 } from 'uuid';
import { Registry } from 'registry.base';
import path from 'path';
import { Either } from 'yl-ddd-ts';

const PROTO_PATH = path.resolve(__dirname, './protos/command-service.proto');

export const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  arrays: true,
});

const commandServiceProto = grpc.loadPackageDefinition(packageDefinition);

export const startService = (registry: Registry) => {
  const server = new grpc.Server();

  server.addService(commandServiceProto.CommandService.service, {
    createCommandWithFile: async (call, callback) => {
      console.log('call', call);
      const result = await registry.commandService.requestCommandWithFile(
        call.request.user_id,
        call.request.command,
        call.request.files.map((f) => ({
          fileName: f.filename,
          content: f.content,
        })),
      )();
      Either.match(
        (e) => {
          console.log('error occured', e);
          callback({
            code: grpc.status.INTERNAL,
            details: e.message,
          });
        },
        (taskId) => {
          console.log('taskId success', taskId);
          callback(null, {
            task_id: taskId,
          });
        },
      )(result);
    },
    createCommandWithInput: async (call, callback) => {
      console.log('command with input', call.request);
      const result = await registry.commandService.requestCommand(
        call.request.user_id,
        call.request.command,
        call.request.input,
      )();
      Either.match(
        (e) => {
          callback({
            code: grpc.status.INTERNAL,
            details: e.message,
          });
        },
        (taskId) => {
          console.log('taskId success', taskId);
          callback(null, {
            task_id: taskId,
          });
        },
      )(result);
    },
  });

  server.bind('127.0.0.1:30043', grpc.ServerCredentials.createInsecure());
  console.log('Server running at http://127.0.0.1:30043');
  server.start();
};
