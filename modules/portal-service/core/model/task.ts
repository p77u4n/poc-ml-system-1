import { Brand, Either, Task } from 'yl-ddd-ts';
import * as Option from 'fp-ts/Option';
import { validate } from 'uuid';
import { P, match } from 'ts-pattern';

export type UUID = Brand<string, 'UUID'>;

export function isUUID(v: string): v is UUID {
  return validate(v);
}

export enum Statuses {
  FINISH = 'FINISH',
  FAILED = 'FAILED',
  PENDING = 'PENDING',
  PROCESSING = 'PROCESSING',
}

function isStatus(v: string): v is Statuses {
  return Object.values(Statuses).includes(v as Statuses);
}

export enum Commands {
  PREDICT = 'PREDICT',
  EXPORT = 'EXPORT',
  LOGS = 'LOGS',
  DATASET_CREATE = 'DATASET_CREATE',
  DOWNLOAD = 'DOWNLOAD',
}

function isCommand(v: string): v is Commands {
  return Object.values(Commands).includes(v as Commands);
}

export interface FileInput {
  fileURIs: string[];
}

function isFileInput(v: Record<string, any>): v is FileInput {
  return Object.keys(v).length === 1 && Array.isArray(v['fileURIs']);
}

export interface PredictInput {
  topLeftX: number;
  topLeftY: number;
  bottomRightX: number;
  bottomRightY: number;
}

function isPredictInput(v: Record<string, any>): v is PredictInput {
  return (
    Object.keys(v).length === 4 &&
    'topLeftX' in v &&
    'topLeftY' in v &&
    'bottomRightX' in v &&
    'bottomRightY' in v
  );
}

export interface Task {
  id: UUID;
  userId: UUID;
  status: Statuses;
  result: Option.Option<string>;
  failReason: Option.Option<string>;
  input: FileInput | PredictInput;
  command: Commands;
}

export const parseTask = (params: {
  id: string;
  userId: string;
  status: string;
  command: string;
  result?: string;
  failReason?: string;
  input: Record<string, any>;
}): Either.Either<Error, Task> => {
  return match([params.userId, params.id, params.command, params.status])
    .with(
      [
        P.select('userId', P.when(isUUID)),
        P.select('id', P.when(isUUID)),
        P.select('command', P.when(isCommand)),
        P.select('status', P.when(isStatus)),
      ],
      ({ userId, command, status, id }) => {
        return match([command, params.input])
          .with(
            P.union(
              [Commands.PREDICT, P.select('input', P.when(isPredictInput))],
              [P._, P.select('input', P.when(isFileInput))],
            ),
            ({ input }) =>
              Either.right({
                id,
                userId,
                status: status,
                result: Option.fromNullable(params.result),
                failReason: Option.fromNullable(params.failReason),
                input,
                command: command,
              } as Task),
          )
          .otherwise(() => Either.left(new Error('COMMAND_INPUT_NOT_MATCH')));
      },
    )
    .otherwise(() =>
      Either.left(
        new Error(`TASK_PROPS_FAILED_VALIDATION: ${JSON.stringify(params)}`),
      ),
    ) as Either.Either<Error, Task>;
};
