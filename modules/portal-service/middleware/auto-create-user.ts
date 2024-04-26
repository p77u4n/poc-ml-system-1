import { isUUID } from 'core/model/task';
import { Request, Response, NextFunction } from 'express';
import { P, match } from 'ts-pattern';
import { postgresDTsource } from 'database-typeorm/datasource';
import { DMUser } from 'database-typeorm/entities';

export async function createUserMiddleware(
  req: Request,
  res: Response,
  next: NextFunction,
) {
  const userId = req.body.userId;
  await match(userId)
    .with(P.when(isUUID), async (id) => {
      const userRepository = postgresDTsource.getRepository(DMUser);
      const dmUser = userRepository.create();
      dmUser.id = id;
      await userRepository.save(dmUser);
    })
    .with(P.nullish, () => Promise.resolve(null))
    .otherwise(() => Promise.reject(new Error('user id must be in uuid')));

  next();
}
