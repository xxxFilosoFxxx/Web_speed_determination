#!/bin/bash

# Ждем БД
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Запускаем создание таблиц в БД
if [ "$PROJECT_ENV" = "prod" ]
then
    echo "Creating the database tables..."
    # сохранить все данные ИЛИ запускать полностью чистым
    python manage.py init_db
    echo "Tables created or already exist"
fi

gunicorn -b 0.0.0.0:8888 -w 4 backend.app:app
