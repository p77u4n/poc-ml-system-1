import { taskRoute } from 'controller/task.controller';
import express from 'express';
import cors from 'cors';
import fileUpload from 'express-fileupload';
import { createUserMiddleware } from 'middleware/auto-create-user';

export const app = express();
const port = 3003;
app.use(
  cors({
    allowedHeaders: '*',
    origin: '*',
    methods: '*',
  }),
);
app.use(fileUpload());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(createUserMiddleware);

app.use(taskRoute);

app.get('/', (req, res) => {
  res.send('Welcome !');
});

export const runExpress = () => {
  app.listen(port, () => {
    console.log(`Example app listening on port ${port}`);
  });
};
