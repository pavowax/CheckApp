FROM node:20-buster

WORKDIR /app

COPY ./app/package.json /app/

COPY ./app .

EXPOSE 3000

CMD npm install && npm start