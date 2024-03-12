from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("config.py")

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


@app.route("/")
def index():
    """Главная страница."""
    return render_template("index.html", title="Главная страница")


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
    session.pop("user_id", None)
    return render_template("logout.html", title="Вы вышли")


if __name__ == "__main__":
    app.run(debug=True)
