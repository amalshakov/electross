from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from app import User, app, db

auth_bp = Blueprint("auth", __name__)
app.register_blueprint(auth_bp)


@auth_bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if not request.form["psw"] == request.form["psw2"]:
            flash("Введенные пароли не совпадают!", "error")
            return redirect(url_for("auth.register"))
        new_user = User(
            username=request.form["username"], email=request.form["email"]
        )
        new_user.set_password(request.form["psw"])
        print("------------ОТЛАДКА-----------------------")
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"})
    return render_template("register.html", title="Регистрация")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if user and user.check_password(data["password"]):
        # Реализуйте здесь генерацию токена аутентификации или сессии
        return jsonify({"message": "Login successful"})
    return jsonify({"message": "Invalid username or password"})


@auth_bp.route("/logout")
def logout():
    # Реализуйте здесь выход пользователя из системы
    return jsonify({"message": "Logged out successfully"})
