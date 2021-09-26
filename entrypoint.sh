sudo service rabbitmq-server start
sudo rabbitmq-plugins enable rabbitmq_management

[Если БД не установлена и нет базы]
#  (Установить psql)
  sudo apt install postgresql postgresql-contrib
#  (Создание базы)
  sudo -u postgres psql
  create database tasks_docs; create database tasks_docs_meta;
  create user test;
  alter database task_docs owner to test; alter database task_docs_meta owner to test;
  alter user test with encrypted password 'test';
#  (migrate БД)
  flask db init
  flask db migrate
  flask db upgrade

export APP_SETTINGS="config.Config"
export DATABASE_URL="postgresql://test:test@localhost/tasks_docs" # Ваш url

[Если другой адрес для очереди задач]
  export CELERY_BROKER_URL="amqp://guest:guest@localhost:5672//" # Ваш url
  export CELERY_RESULT_BACKEND="db+postgresql+psycopg2://test:test@localhost/tasks_docs" # Ваш url
