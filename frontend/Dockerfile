ARG NODE_VERSION=20

FROM node:${NODE_VERSION}-slim as base

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

RUN npm run build
CMD [ "node", ".output/server/index.mjs" ]