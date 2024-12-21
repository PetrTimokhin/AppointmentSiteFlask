from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import uuid
from flask_login import LoginManager

from config import DATABASE_URI, SECRET_KEY

# Создание экземпляра приложения Flask и настройка
# его основных параметров и подключения к базе данных
app = Flask(__name__)
# Настройка поддержки вебсокетов
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
# создание ключа flask_login LoginManager
app.config['SECRET_KEY'] = SECRET_KEY
# Инициализация базы данных
db = SQLAlchemy(app)
# Инициализация менеджера логина
manager = LoginManager(app)
