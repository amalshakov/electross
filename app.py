import MySQLdb
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_bcrypt import Bcrypt
from flask_login import current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

#! Запуск локально c локальной MySQL
# app.config.from_pyfile("config.py")

#! Запуск на pythonanywhere.com c MySQL
# https://docs.google.com/document/d/1dUdxvvzTsHr5pNZ0UZmjD92yoHshmqvePVdrh6mlavU/edit?pli=1#heading=h.pjlds4jwmyzk
# https://docs.google.com/document/d/1I-u3xEnfjRc2ClWxtNy8lE0Sm2K9UMxRGBprJ4YwDeY/edit?pli=1#heading=h.73h4paph2n9g
# https://help.pythonanywhere.com/pages/Virtualenvs
# https://www.pythonanywhere.com/batteries_included/
# Выше инструкции по которым делать
# 1. Через git залить проект на pythonanywhere
# 2. Сделать дамп базы и разместить на pythonanywhere. Настроить
# 3. Виртуальное окружение. Установить зависимости.
# 4. Внести изменения в app.py
app = Flask(__name__)
app.config["SECRET_KEY"] = "qwerty123QWERTY321"
userpass = "mysql://morongod:mysqlpsw@"
basedir = "morongod.mysql.pythonanywhere-services.com"
dbname = "/morongod$electross_db"
app.config["SQLALCHEMY_DATABASE_URI"] = userpass + basedir + dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


migrate = Migrate(app, db)
bcrypt = Bcrypt()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)

    def set_password(self, password):
        """Сохраняет пароль в зашифрованном виде."""
        self.password_hash = bcrypt.generate_password_hash(password).decode(
            "utf-8"
        )

    def check_password(self, password):
        """Проверяет пароль."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return self.username


class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    birth_day = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


@app.route("/edit_cat/<int:cat_id>", methods=["GET", "POST"])
def edit_cat(cat_id):
    """Редактировать созданный экземпляр класса Cat."""
    cat = Cat.query.get(cat_id)

    if request.method == "POST":
        cat.name = request.form["name"]
        cat.color = request.form["color"]
        cat.birth_day = request.form["birth_day"]
        cat.description = request.form["description"]
        db.session.commit()
        return redirect(url_for("index"))

    return render_template(
        "edit_cat.html", cat=cat, title="Редактирование кота"
    )


@app.route("/delete_cat/<int:cat_id>", methods=["DELETE"])
def delete_cat(cat_id):
    """Удалить созданный экземпляр класса Cat."""
    cat = Cat.query.get(cat_id)
    db.session.delete(cat)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/add_cat", methods=["POST"])
def add_cat():
    """Создать экземпляр класса Cat."""
    name = request.form["name"]
    color = request.form["color"]
    birth_day = request.form["birth_day"]
    description = request.form["description"]
    owner_id = request.form["owner_id"]

    new_cat = Cat(
        name=name,
        color=color,
        birth_day=birth_day,
        description=description,
        owner_id=owner_id,
    )
    db.session.add(new_cat)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/cats/<int:cat_id>")
def cat(cat_id):
    """Предоставляет информацию о конкретном объекте класса Cat."""
    cat = Cat.query.get(cat_id)
    return render_template("cat.html", cat=cat, title=cat.name)


@app.route("/")
def index():
    """Главная страница."""
    cats = Cat.query.all()
    return render_template("index.html", title="Главная страница", cats=cats)


@app.route("/register", methods=["POST", "GET"])
def register():
    """Регистрация."""
    if "user_id" in session:
        return redirect(url_for("index"))
    if request.method == "POST":
        if not request.form["psw"] == request.form["psw2"]:
            flash("Введенные пароли не совпадают!", "error")
            return redirect(url_for("register"))
        existing_user = User.query.filter_by(
            username=request.form["username"]
        ).first()
        if existing_user:
            flash("Пользователь с таким именем уже существует!", "error")
            return redirect(url_for("register"))
        new_user = User(
            username=request.form["username"], email=request.form["email"]
        )
        new_user.set_password(request.form["psw"])
        db.session.add(new_user)
        db.session.commit()
        return render_template("successregister.html", title="Успех")
    return render_template("register.html", title="Регистрация")


@app.route("/login", methods=["POST", "GET"])
def login():
    """Авторизация."""
    if "user_id" in session:
        return redirect(url_for("index"))
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and user.check_password(request.form["psw"]):
            session["user_id"] = user.id
            return render_template("successlogin.html", title="Успех")
        return render_template("badlogin.html", title="Fail")
    return render_template("login.html", title="Войти")


@app.route("/logout")
def logout():
    """Выход из системы."""
    session.pop("user_id", None)
    return render_template("logout.html", title="Вы вышли")


if __name__ == "__main__":
    app.run(debug=True)
