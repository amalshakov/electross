# electross
Тестовое задание
Разработка простого веб-приложения с использованием Python, Flask, и MySQL:
Вам предлагается разработать простое веб-приложение, которое будет включать в себя следующие функции:
1.	Регистрация и аутентификация пользователей:
•	Разработайте систему регистрации и аутентификации пользователей с использованием Flask и MySQL.
2.	CRUD операции с данными:
•	Реализуйте возможность создания, чтения, обновления и удаления данных пользователями через веб-интерфейс.
3.	Работа с базой данных MySQL:
•	Опишите процесс создания базы данных и таблиц в MySQL для хранения данных пользователей.
•	Разработайте SQL запросы для выполнения CRUD операций.
4.	Разработка фронтенд компонентов:
•	Разработайте простой пользовательский интерфейс для взаимодействия с веб-приложением.

#  Работа с репозиторием
- клонируйте репозиторий
```
git clone git@github.com:amalshakov/electross.git
```
- Перейдите в папку с проектом, создайте виртуальное окружение.
```
python -m venv venv
```
- Установите зависимости (библиотеки)
```
pip install -r requirements.txt
```
- Используйте (запустите) локально базу MySQL. Создайте базу данных.
- В файле конфигурации (config.py), указаны следующие параметры для подключения к базе данных:
```
SQLALCHEMY_DATABASE_URI = "mysql://root:mysqlpsw@localhost/electross_db"
```
- При необходимости замените их
```
SQLALCHEMY_DATABASE_URI = "mysql://<myuser>:<mypassword>@localhost/<mydatabase>"
```
Где myuser и mypassword - это имя пользователя и пароль, а mydatabase - имя вашей базы данных.
- Выполните миграции. Создайте таблицы в БД.
```
flask db init
flask db migrate
flask db upgrade
```
- Запустите локально сервер (запустите файл app.py)
- В проекте 2 модели:
    - User (пользователи)
    - Cat (коты. Пользователь может создавать экземпляр класса Cat, редактировать, удалять)
- Эндпоинты:
    - "/register"    
        - Для регистрации пользователя (создания экземпляра класса User)
    - "/login"
        - Для авторизации пользователя
    - "/logout"
        - Разлогиниться (пользователю)
    - "/add_cat"
        - Создать экземпляр класса Cat (для авторизированного пользователя)
    - "/edit_cat/<int:cat_id>"
        - Редактировать экземпляр класса Cat (для авторизированного пользователя, при условии, что он является "владельцем")
    - "/delete_cat/<int:cat_id>"
        - Удалить экземпляр класса Cat (для авторизированного пользователя, при условии, что он является "владельцем")
    - "/"
        - Главная страница, с интерфейсом для регистрации, авторизации, выхода пользователя из системы. Формой для создания экземпляра класса Cat. Выводом информации о всех созданных экземплярах класса Cat.
    - "/cats/<int:cat_id>"
        - Вывод информации о конкретном экземпляре класса Cat.

# Технологии:
- Flask-Bcrypt==1.0.1
- Flask-SQLAlchemy==3.1.1
- Flask==3.0.2
- mysqlclient==2.2.4
- Flask-Login==0.6.3
- Flask-Migrate==4.0.6
- Flask-MySQLdb==2.0.0
- Flask-Script==2.0.6

# Запуск локально c локальной MySQL
- app.config.from_pyfile("config.py")

# Запуск на pythonanywhere.com c MySQL
- https://docs.google.com/document/d/1dUdxvvzTsHr5pNZ0UZmjD92yoHshmqvePVdrh6mlavU/edit?pli=1#heading=h.pjlds4jwmyzk
- https://docs.google.com/document/d/1I-u3xEnfjRc2ClWxtNy8lE0Sm2K9UMxRGBprJ4YwDeY/edit?pli=1#heading=h.73h4paph2n9g
- https://help.pythonanywhere.com/pages/Virtualenvs
- https://www.pythonanywhere.com/batteries_included/
- Выше инструкции по которым делать
- 1. Через git залить проект на pythonanywhere
- 2. Сделать дамп базы и разместить на pythonanywhere. Настроить
- 3. Виртуальное окружение. Установить зависимости.
- 4. Внести изменения в app.py
- app = Flask(__name__)
- app.config["SECRET_KEY"] = "qwerty123QWERTY321"
- userpass = "mysql://morongod:mysqlpsw@"
- basedir = "morongod.mysql.pythonanywhere-services.com"
- dbname = "/morongod$electross_db"
- app.config["SQLALCHEMY_DATABASE_URI"] = userpass + basedir + dbname
- app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
- db = SQLAlchemy(app)