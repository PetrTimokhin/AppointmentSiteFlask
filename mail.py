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


# send_email('Привет, готов к уроку?', 'ptimohin01@gmail.com ', 'Занятие')




# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
#
# from config import MY_MAIL, MY_MAIL_PASSWORD
#
# EMAIL_LOGIN = MY_MAIL
# EMAIL_PASSWORD = MY_MAIL_PASSWORD
#
# msg = MIMEMultipart()
#
# to_email = 'ptimohin@bk.ru'
# message = 'Сообщение сделано при помощи пайтон'
#
# msg.attach(MIMEText(message, 'plain'))
# server = smtplib.SMTP('smtp.yandex.ru: 465')
# server.starttls()
# server.login(MY_MAIL, MY_MAIL_PASSWORD)
# server.sendmail(MY_MAIL, to_email, msg.as_string())
#
# server.quit()


