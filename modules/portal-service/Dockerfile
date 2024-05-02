FROM node:18 as node-app-base

WORKDIR /usr/src/app
EXPOSE 3000

RUN corepack enable
RUN yarn set version 4.1.1
COPY package.json package.json
COPY yarn.lock yarn.lock
COPY .yarnrc.yml .yarnrc.yml

RUN yarn

FROM node-app-base as builder-base

COPY . .

RUN yarn build

FROM builder-base

EXPOSE 3003

CMD yarn service:start

