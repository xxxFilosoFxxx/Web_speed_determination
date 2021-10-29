FROM python:3.8.5-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED=1
#ENV MONGO_HOST=items_db
RUN apt-get update && apt-get install 'ffmpeg' 'libsm6' 'libxext6' 'build-essential' 'cmake' -y

WORKDIR /app
COPY ./backend/ ./
COPY ./manage.py ./
RUN pip install -U pip
RUN pip install -r ./backend/requirements.txt

#COPY ./mongo_client.py /usr/local/lib/python3.9/site-packages/pymongo/mongo_client.py
#COPY ./mongo_client.py /app/venv/lib/python3.8/site-packages/pymongo/mongo_client.py
#COPY --from=static /app/dist/inventorybase/static/css /app/inventorybase/static/css
#COPY --from=static /app/dist/inventorybase/static/js /app/inventorybase/static/js
#COPY --from=static /app/dist/index.html /app/templates/
#ENTRYPOINT ["gunicorn", "-e", "APP_SETTINGS=backend.config.Config", "-b", "0.0.0.0:8888", "-w", "4", "backend.app:app"]
COPY ./entrypoint.sh ./
ENTRYPOINT ["./entrypoint.sh"]