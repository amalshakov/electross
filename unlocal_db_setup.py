#! Эти данные уже размещаем в app на pythonanywhere

import MySQLdb
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config["SECRET_KEY"] = "qwerty123QWERTY321"
userpass = "mysql://root:mysqlpsw@"
basedir = "morongod.mysql.pythonanywhere-services.com"
dbname = "/morongod$electross_db"
app.config["SQLALCHEMY_DATABASE_URI"] = userpass + basedir + dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


@app.route("/")
def testdb():
    if db.session.query(text("1")).from_statement(text("SELECT 1")).all():
        return "It works."
    else:
        return "Something is broken."


if __name__ == "__main__":
    app.run(debug=True)
