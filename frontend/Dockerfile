# Use Node official image
FROM node:20

WORKDIR /cabana

COPY ./cabana/package*.json ./
RUN yarn install

COPY ./cabana .

EXPOSE 3000
CMD ["yarn", "dev"]