FROM python:3.8.5-slim-buster
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install 'ffmpeg' 'libsm6' 'libxext6' 'build-essential' 'cmake' -y

WORKDIR /app
COPY ./backend/ ./
COPY ./manage.py ./
RUN pip install -U pip
RUN pip install -r ./backend/requirements.txt
COPY ./entrypoint.sh ./
#ENTRYPOINT ["./entrypoint.sh"]