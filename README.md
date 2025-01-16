## AppointmentSiteFlask
Сайт для записи на прием к психологу.

## Использованные технологии: 

![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
<br>

## Прежде всего:
> Установите Python (если он не установлен)<br>
> [Скачать Python3](https://www.python.org/downloads/)

<br>

Клонируйте репозиторий и перейдите в установленную папку:
```
git clone https://github.com/PetrTimokhin/AppointmentSiteFlask.git
cd AppointmentSiteFlask
```

Установите requirements:
```
pip3 install -r requirements.txt
```
<br>

Далее вам необходимо создать файл config.py и указать информацию в формате:
```
# для БД (в данном случае sqlite), у вас может быть любая БД
DATABASE_URI = 'sqlite:///наши данные'
# ваша почта с которой будет отправляться письмо для проверки email нового пользователя
EMAIL_LOGIN = 'ваша почта'
# Пароль для внешних приложений вашего почтового сервиса (например mail.ru)
EMAIL_PASSWORD = 'ваши данные'
# ключ flask_login LoginManager
SECRET_KEY = "ваши данные"
```

Тепепрь можно запустить проект командой:
```
python3 main.py
```

## Описание проекта:

На главной странице вам педоставляется календарь с выбором даты посещения и предоставляемой услуге. 
Также есть станичка личного кабинета, где каждый клиент может посмотреть все свои записи. 
При авторизации как admin, на страничке личного кабинете вам будет предоставлена инфформация о всех записях всех клиентов.
