""" Файл для реализации проверки email при регистрации"""


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import EMAIL_LOGIN, EMAIL_PASSWORD


def get_msg(to: str, subject: str):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_LOGIN
    msg['To'] = to
    msg['Subject'] = subject
    return msg


def send_email(message: str, to: str, subject: str):
    msg = get_msg(to, subject)

    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.mail.ru', 25)
    server.starttls()

    server.login(EMAIL_LOGIN, EMAIL_PASSWORD)
    server.sendmail(EMAIL_LOGIN, msg['To'], msg.as_string())

    server.quit()


