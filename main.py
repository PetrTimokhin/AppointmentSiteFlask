from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# создание БД
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


# создание модели БД
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# подключение БД
with app.app_context():
    db.create_all()


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('name')
        password = request.form.get('pswd')
        # tel = request.form.get('tel')

        # Создание данных
        user = User(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            print(f'Успешная регистрация! {user.email}, {user.password}')
            return redirect(url_for('index'))
        print(f'Ошибка регистрации! Попробуйте еще раз!')
    return render_template("auth.html")


@app.route('/login', methods=['POST'])
def login():

    email = request.form.get('email')
    # username = request.form.get('name')
    password = request.form.get('pswd')
    # Чтение данных
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        print(f'Успешная авторизация! {user.email}, {user.password}')
        return redirect(url_for('index'))
    print(f'Ошибка авторизации! Зарегистрируйтесь!')
    return redirect(url_for("register"))


if __name__ == "__main__":
    app.run(debug=True)
