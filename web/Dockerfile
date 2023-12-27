FROM node:20.10.0-buster AS builder

WORKDIR /app

COPY ./app/package.json /app/

COPY ./app .

CMD npm install && npm start