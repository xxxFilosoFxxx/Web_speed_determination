import os


class Config(object):
    DEBUG = False if os.getenv('PROJECT_ENV') == 'prod' else True
    TESTING = False
    LOG_PATH = os.path.abspath(os.path.dirname(__file__)) + '/error.log'
    CSRF_ENABLES = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://test:test@localhost/tasks_docs')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://guest:guest@localhost:5672//')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND',
                                           'db+postgresql://test:test@localhost/tasks_docs')
    # ВОЗМОЖНО -> db+postgresql+psycopg2://test:test@localhost/tasks_docs_meta
    # CELERY_RESULT_DB_TABLE_NAMES = {'task': 'celery', 'group': 'celery', }
