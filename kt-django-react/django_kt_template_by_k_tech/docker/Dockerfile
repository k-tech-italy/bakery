FROM node:16


ADD . /code

WORKDIR /code/frontend

RUN npm install

ENTRYPOINT [ "npm", "run", "dev" ]