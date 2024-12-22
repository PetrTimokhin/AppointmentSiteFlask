import random
import string

from flask import render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user

from app import app, db
from models import User, EmailConfirm, UserAppointData
from mail import send_email


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
@login_required
def index():
    actual_user = User.query.filter_by(id=current_user.id).first()
    if request.method == 'POST':
        # client_name = request.form.get('client_name')
        phone_number = request.form.get('phone_number')
        date = request.form.get('date')
        time = request.form.get('time')
        service = request.form.get('service')
        user_appointment = UserAppointData(
                                            client_name=actual_user.login,
                                            phone_number=phone_number,
                                            date=date,
                                            time=time,
                                            service=service,
                                            user_id=actual_user.id)
        db.session.add(user_appointment)
        db.session.commit()
        print(user_appointment.service)
        return redirect(url_for('client'))

    return render_template("index.html",
                           client_name=current_user.login)

# user = request.args.get('user')


@app.route("/register", methods=['GET', 'POST'])
def register():
    # страницу регистрации заменяет страница авторизации для авторизованных
    if current_user.is_authenticated:
        return render_template("login.html")

    elif request.method == 'POST':
        # принимаем данные форм с html страницы
        email = request.form.get('email')
        username = request.form.get('login')
        password = request.form.get('password')

        # проверка на уникальность имени и email
        if (User.query.filter_by(login=username).first()
                or User.query.filter_by(email=email).first()):
            message = "Такое имя или email уже используются!!!"
            return render_template("register.html", message=message)

        try:
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

        except:
            message = "Ошибка ввода данных!"
            return render_template("register.html", message=message)
    return render_template("register.html")


@app.route('/email-confirm/<code>')
# Функция для подтверждения email
def email_confirm(code):
    # Проверяем, существует ли подтверждение с таким кодом в БД
    user_confirm = EmailConfirm.query.filter_by(code=code).first()
    # Если подтверждение существует, то удаляем его из БД и меняем статус
    # email_confirm у пользователя в БД
    if user_confirm:
        # Ищем пользователя в БД по логину, соответствующему логину
        # в подтверждении
        user = User.query.filter_by(login=user_confirm.login).first()
        # Если пользователь найден, то меняем его поле email_confirm
        # в БД на значение True
        user.email_confirm = True
        # Добавляем пользователя в БД
        db.session.add(user)
        # Удаляем подтверждение почты из БД
        db.session.delete(user_confirm)
        # Сохраняем изменения в БД
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    # Возвращаемся на страницу index
    return redirect(url_for('register'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # email = request.form.get('email')
        username = request.form.get('login')
        password = request.form.get('password')
        # Чтение данных
        user = User.query.filter_by(login=username, password=password).first()
        if user and user.email_confirm:
            login_user(user)
            return redirect(url_for('index'))
    return render_template("login.html")


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.login == "admin":
        all_users_id_lst = []
        all_users = User.query.all()
        print(type(all_users))
        for each in all_users:
            all_users_id_lst.append(each.id)

        print(all_users_id_lst)
        everyone_appointments = UserAppointData.query.all()
        return render_template("admin.html",
                               appointments=everyone_appointments,
                               all_users=all_users,
                               User=User,
                               all_users_id_lst=all_users_id_lst)


@app.route("/client", methods=['GET', 'POST'])
@login_required
def client():
    if current_user.login == "admin":
        return redirect("/admin")
    else:
        appointments = UserAppointData.query.filter_by(
            user_id=current_user.id).all()

        return render_template("client.html",
                               appointments=appointments,
                               client_name=current_user.login)


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


@app.route('/base')
def base():
    return render_template("base.html")

