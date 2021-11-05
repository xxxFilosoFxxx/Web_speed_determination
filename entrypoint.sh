#!/bin/bash

# Wait for db
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# run create db
if [ "$PROJECT_ENV" = "prod" ]
then
    echo "Creating the database tables..."
    # TODO
    # Очистить папку media, если такая есть
    # Очистить таблицу celery_task (удалить и заново создать)
    python manage.py init_db
    echo "Tables created"
fi

gunicorn -b 0.0.0.0:8888 -w 4 backend.app:app
