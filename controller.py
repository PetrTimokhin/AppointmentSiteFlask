import random
import string

from flask import render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user

from app import app, db
from models import User, EmailConfirm
from mail import send_email


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/email-confirm/<code>')
def email_confirm(code):
    user_confirm = EmailConfirm.query.filter_by(code=code).first()
    if user_confirm:
        user = User.query.filter_by(login=user_confirm.login).first()
        user.email_confirm = True
        db.session.add(user)
        db.session.delete(user_confirm)
        db.session.commit()
    return redirect(url_for('register'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('login')
        password = request.form.get('password')
        # tel = request.form.get('tel')

        # Создание данных
        user = User(email=email, login=username, password=password)
        code = ''.join(
            [random.choice(string.ascii_letters + string.digits) for i in
             range(32)])
        user_confirm = EmailConfirm(login=username, code=code)
        db.session.add(user)
        db.session.add(user_confirm)
        db.session.commit()

        message = (f'Ссылка для подтверждения '
                   f'почты: http://127.0.0.1:5000/email-confirm/{code}')

        send_email(message, email, 'Подтверждение почты')
        # login_user(user)
        # user = User.query.filter_by(email=email, password=password).first()
        # if user:
        #     print(f'Успешная регистрация! {user.email}, {user.password}')
        #     return redirect(url_for('index'))
        # print(f'Ошибка регистрации! Попробуйте еще раз!')
    return render_template("auth.html")


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    # username = request.form.get('name')
    password = request.form.get('password')
    # Чтение данных
    user = User.query.filter_by(email=email, password=password).first()
    if user and user.email_confirm:
        login_user(user)
        print(f'Успешная авторизация! {user.email}, {user.password}')
        return redirect(url_for('index'))
    print(f'Ошибка авторизации! Зарегистрируйтесь!')
    return redirect(url_for("register"))


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    return render_template("admin.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('register'))
    return response
