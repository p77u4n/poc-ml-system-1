FROM node:18 as builder

WORKDIR /app

COPY package.json package.json
COPY .yarnrc.yml .yarnrc.yml
COPY yarn.lock yarn.lock

RUN corepack enable
RUN yarn set version 4.1.1

RUN yarn

COPY . .

COPY .build.env .env

RUN yarn build

FROM node:18 as runner

WORKDIR /app

COPY --from=builder /app/build build

RUN yarn global add serve

EXPOSE 3000

CMD ["serve", "-s", "build"]
