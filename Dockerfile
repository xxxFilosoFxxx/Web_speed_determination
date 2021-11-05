FROM node:16-alpine as build-stage
WORKDIR /app
COPY ./package.json .
COPY ./vue.config.js .
COPY ./babel.config.js .
COPY ./public ./public/
COPY ./src ./src/
RUN npm install
RUN npm run build

FROM python:3.8.5-slim-buster
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install 'ffmpeg' 'libsm6' 'libxext6' 'build-essential' 'cmake' 'netcat' -y
WORKDIR /app
COPY --from=build-stage /app/dist ./dist/
COPY ./requirements.txt ./requirements.txt
RUN pip install -U pip
RUN pip install -r ./requirements.txt
COPY ./backend/ ./backend/
COPY ./manage.py .
COPY ./entrypoint.sh .