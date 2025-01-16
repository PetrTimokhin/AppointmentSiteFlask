"""Файл для работы со всеми контроллерами проекта"""


import random
import string

from flask import render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from flask.wrappers import Response

from app import app, db
from models import User, EmailConfirm, UserAppointData
from mail import send_email


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index() -> Response or str:
    """
    Функция главной страницы сайта

    Обработчик для страницы index.html, где аутентифицированный пользователь
    может создать новую запись. При GET-запросе отображается форма, а при
    POST-запросе данные формы обрабатываются и сохраняются в базе данных,
    после чего пользователь перенаправляется на страницу client.html

    Returns:
        str: шаблон страницы index.html
        Response: перенаправление на функцию def client
    """
    actual_user = User.query.filter_by(id=current_user.id).first()
    if request.method == 'GET':
        return render_template('index.html',
                               client_name=current_user.login)
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
    return redirect(url_for('client'))


@app.route('/register', methods=['GET', 'POST'])
def register() -> str:
    """
    Функция обработчик страницы register.html

    Если пользователь уже зарегистрирован, то он перенаправляется на страницу
    login.html;
    При GET-запросе отображается форма register.html. При POST-запросе: данные
    формы обрабатываются, проверяются на уникальность и сохраняются в базе
    данных. Затем в этой функции генерируется код для проверки email, который
    подставляется в ссыку, высланную на указанную эл почту при регистрации.
    Затем запускается функция email_confirm;
    При ошибке ввода данных функция перенаправляет на страницу register.html;

    Returns:
        str: шаблон страницы register.html
    """
    # страницу регистрации заменяет страница авторизации для авторизованных
    if current_user.is_authenticated:
        return render_template('login.html')
    if request.method == 'GET':
        return render_template('register.html')

    # принимаем данные форм с html страницы
    email = request.form.get('email')
    username = request.form.get('login')
    password = request.form.get('password')

    # проверка на уникальность имени и email
    if (User.query.filter_by(login=username).first()
            or User.query.filter_by(email=email).first()):
        message = 'Такое имя или email уже используются!!!'
        return render_template('register.html', message=message)

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
        message = 'Ошибка ввода данных!'
        return render_template('register.html', message=message)


@app.route('/email-confirm/<code>')
# Функция для подтверждения email
def email_confirm(code: str) -> Response:
    """
    Функция подтверждения email пользователя

    Функция находит в БД пользователя с кодом переданным в функцию. Если такой
    пользователь найден, сохраняет в БД информацию, что пользователь прошел
    подтверждение email, и удаляет из БД сгенерированный код. Далее запускается
    функция login_user(user) от имени этого пользователя, что завершает процесс
    регистрации, перенаправляя пользователя в функцию index;
    Если пользователь с данным кодом не найден, то данная функция
    перенаправляет на функцию register;

    Args:
        code: str (описание)

    Returns:
        Response: перенаправление на функцию def index
        Response: перенаправление на функцию def register
    """
    # Проверяем, существует ли подтверждение с таким кодом в БД
    user_confirm = EmailConfirm.query.filter_by(code=code).first()
    # Если подтверждение существует, то удаляем его из БД и меняем статус
    # email_confirm у пользователя в БД
    if not user_confirm:
        # Возвращаемся на страницу register
        return redirect(url_for('register'))
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
    # специальная функция импортируемая из flask-login
    login_user(user)
    # Возвращаемся на страницу index
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Функция обработчик страницы login.html

    При GET-запросе отображается форма login.html. При POST-запросе: данные
    формы обрабатываются, если пользователь с такими данными найден в БД и он
    зарегистрирован, то данная функция запускает функцию login_user, что
    делает данного пользователя авторизированным, и перенаправляет
    в функцию index;
    При ошибке ввода данных функция перенаправляет на страницу login.html;

    Returns:
        Response: перенаправление на функцию def index
        str: шаблон страницы login.html
    """
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('login')
    password = request.form.get('password')
    # Чтение данных
    user = User.query.filter_by(login=username, password=password).first()
    if user and user.email_confirm:
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin() -> str or Response:
    """
    Функция обработчик страницы admin.html

    Функция работает только с пользователем admin. Перенаправляет на страницу
    admin.html, на которой предоставляет данные обо всех записях всех
    пользователей;

    Returns:
        Response: перенаправление на функцию def client
        str: шаблон страницы admin.html
    """
    if current_user.login != 'admin':
        return redirect(url_for('client'))

    all_users_id_lst = []
    all_users = User.query.all()
    for each in all_users:
        all_users_id_lst.append(each.id)

    everyone_appointments = UserAppointData.query.all()
    return render_template('admin.html',
                           appointments=everyone_appointments,
                           all_users=all_users,
                           User=User,
                           all_users_id_lst=all_users_id_lst)


@app.route('/client', methods=['GET', 'POST'])
@login_required
def client() -> str or Response:
    """
    Функция обработчик страницы client.html

    Функция проверяет имя текущего пользователя, если оно admin, то
    перенаправляет в функцию admin, если нет, то перенаправляет на
    страницу client.html, на которой предоставляет данные обо всех записях
    текущего пользователя;

    Returns:
        Response: перенаправление на функцию def admin
        str: шаблон страницы client.html
    """
    if current_user.login == 'admin':
        return redirect(url_for('admin'))

    appointments = UserAppointData.query.filter_by(
        user_id=current_user.id).all()

    return render_template('client.html',
                           appointments=appointments,
                           client_name=current_user.login)


@app.route('/logout')
@login_required
def logout() -> Response:
    """
    Функция обработчик страницы logout.html

    Данная функция делает текущего пользователя не авторизированным и
    перенаправляет на функцию index;

    Returns:
        Response: перенаправление на функцию def index
    """
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_sign(response: Response) -> Response:
    """
    Обработка ответа с кодом статуса 401;

    Функция запускается после обработки каждого запроса, но до того, как будет
    отправлен ответ клиенту. Когда приходит ответ с кодом статуса 401
    (несанкционирован), он автоматически перенаправляет пользователя на
    страницу регистрации. Если код статуса отличен от 401, то ответ остается
    неизменным.

    Returns:
        Response: перенаправление на функцию def register
        Response: возвращает переменную response в неизменном виде
    """
    if response.status_code == 401:
        return redirect(url_for('register'))
    return response
