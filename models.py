"""Файл для работы с БД"""


from datetime import datetime
from flask_login import UserMixin

from app import app, db, manager


class EmailConfirm(db.Model):
    """
    Класс объекта БД

    Класс для сохранения в БД сгенерированного кода для проверки email нового
    зарегистрированного пользователя;
    """
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    code = db.Column(db.String(33), unique=True, nullable=False)


# создание модели БД,
# добавляем родительский класс UserMixin для flask_login
class User(db.Model, UserMixin):
    """
    Класс объекта БД

    Класс для сохранения в БД данных нового зарегистрированного пользователя:
    id клиента, email, имя, пароль для авторизации, подтверждение проверки
    email, дата и время внесения данных в БД;
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True)
    login = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(64))
    email_confirm = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class UserAppointData(db.Model):
    """
    Класс объекта БД

    Класс для сохранения в БД данных о записи клиента: дата записи, время,
    выбранная услуга, номер телефона, id клиента, имя клиента;
    """
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(90))
    phone_number = db.Column(db.Integer)
    date = db.Column(db.String(20))
    time = db.Column(db.String(10))
    service = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# подключение БД
with app.app_context():
    db.create_all()


# Загрузка пользователя из БД
@manager.user_loader
def load_user(user_id: int) -> User:
    """
    Функция для загрузки пользователя из базы данных;

    Данная функция предназначена для управления сессиями пользователей и
    обеспечения доступа к данным пользователя во время запросов;
    """
    return User.query.get(user_id)  # user_id это id = db.Column
