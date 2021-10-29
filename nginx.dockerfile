FROM node:16-alpine as build-stage
WORKDIR /app
COPY ./package.json .
COPY ./vue.config.js .
COPY ./babel.config.js .
COPY ./public ./public/
COPY ./src ./src/
RUN npm install
RUN npm run build

FROM nginx:latest
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY --from=build-stage /app/dist /app/dist/