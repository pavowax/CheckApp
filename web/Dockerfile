FROM node:latest

WORKDIR /app

COPY ./app/package.json /app/

COPY ./app .

EXPOSE 3000

CMD npm install && npm start