from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import uuid
from flask_login import LoginManager

from config import DATABASE_URI

app = Flask(__name__)
# создание БД
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
# создание ключа flask_login LoginManager
app.config['SECRET_KEY'] = "csfvvasdvq2323123"
# создание БД
db = SQLAlchemy(app)
# создание LoginManager
manager = LoginManager(app)
