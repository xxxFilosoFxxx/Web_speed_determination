import datetime

from werkzeug.security import generate_password_hash,  check_password_hash
from flask_login import UserMixin
from flask_script import Command
from app import db, login


class Result(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, nullable=False)
    msisdn = db.Column(db.Float, nullable=False)
    radius = db.Column(db.Float, nullable=False)
    delta = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

    def __init__(self, uuid: str, msisdn: float, radius: float, delta: float):
        self.uuid = uuid
        self.msisdn = msisdn
        self.radius = radius
        self.delta = delta
        self.total = (radius + delta) * msisdn

    def __repr__(self):
        return f'<id: {self.id}>{self.uuid}, ({self.radius} + {self.delta}) * {self.msisdn} = {self.total}>'


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    updated_on = db.Column(db.DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

    def __init__(self, username: str):
        self.username = username

    def __repr__(self):
        return f'<{self.id}:{self.username}>'

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self,  password: str):
        return check_password_hash(self.password_hash, password)


class InitDbCommand(Command):
    def run(self):
        print("Создание таблиц в базе данных...")
        init_db()
        print('Таблицы созданы!')


def init_db():
    db.drop_all()
    db.create_all()


@login.user_loader
def load_user(user_id: int):
    return User.query.get(user_id)
