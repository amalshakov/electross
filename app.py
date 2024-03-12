from flask import Flask
from flask_bcrypt import Bcrypt
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


if __name__ == "__main__":
    app.run(debug=True)
