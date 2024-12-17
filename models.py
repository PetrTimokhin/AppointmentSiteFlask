from datetime import datetime

from flask_login import UserMixin

from app import app, db, manager


class EmailConfirm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    code = db.Column(db.String(33), unique=True, nullable=False)


# создание модели БД
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True)
    login = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(64))
    email_confirm = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# подключение БД
with app.app_context():
    db.create_all()


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)  # user_id это id = db.Column
