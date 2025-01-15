""" Файл для реализации проверки email при регистрации"""


import smtplib  # библиотека smtplib, которая предоставляет функциональность
# для работы с протоколом SMTP (Simple Mail Transfer Protocol), используемым
# для отправки электронной почты.
from email.mime.text import MIMEText  # Этот класс используется для создания
# MIME-сообщений, содержащих простой текстовый контент.
from email.mime.multipart import MIMEMultipart  # Этот класс используется для
# создания составных MIME-сообщений, которые могут содержать текст, вложения
# и другие типы контента.

from config import EMAIL_LOGIN, EMAIL_PASSWORD


def get_msg(to: str, subject: str) -> MIMEMultipart:
    """
    Функция создает и подготавливает основу для MIME-сообщения.

    Функция создает новый объект MIMEMultipart, который будет использоваться
    для формирования сообщения. Устанавливает заголовок “From” сообщения,
    указывая адрес электронной почты отправителя (взятый из переменной
    EMAIL_LOGIN). Устанавливает заголовок “To” сообщения, указывая адрес
    электронной почты получателя (переданный в аргументе to). Устанавливает
    заголовок “Subject” сообщения, указывая тему письма (переданную в
    аргументе subject). Возвращает созданный объект MIMEMultipart,
    представляющий основу сообщения.

    Args:
        to: str (адрес электронной почты получателя)
        subject: str (тема письма)

    Returns:
        MIMEMultipart: созданный объект MIMEMultipart
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL_LOGIN
    msg['To'] = to
    msg['Subject'] = subject
    return msg


def send_email(message: str, to: str, subject: str) -> None:
    """
    Эта функция отвечает за отправку электронной почты.

    Функция вызывает функцию get_msg для создания основы MIME-сообщения с
    указанными получателем 'To' и темой 'Subject'. Создает объект MIMEText с
    текстом письма (переданным в аргументе message) и типом ‘plain’
    (простой текст). Затем этот объект добавляется в качестве вложения к
    основному сообщению (msg). Создает объект SMTP, который устанавливает
    соединение с SMTP-сервером smtp.mail.ru на порту 25 (mail.ru). ключает
    шифрование TLS (Transport Layer Security) для обеспечения безопасной
    передачи данных с сервером. Выполняет аутентификацию на SMTP-сервере,
    используя учетные данные (адрес электронной почты и пароль), сохраненные в
    переменных EMAIL_LOGIN и EMAIL_PASSWORD. Отправляет сообщение. Первый
    аргумент - адрес отправителя, второй - адрес получателя, третий -
    сформированное сообщение в виде строки. Закрывает соединение с SMTP-
    сервером.

    Args:
        message: str (текст письма)
        to: str (адрес электронной почты получателя)
        subject: str (тема письма)

    """
    msg = get_msg(to, subject)

    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.mail.ru', 25)
    server.starttls()

    server.login(EMAIL_LOGIN, EMAIL_PASSWORD)
    server.sendmail(EMAIL_LOGIN, msg['To'], msg.as_string())

    server.quit()


