from flask import Flask
from flask_mysqldb import MySQL
from flask_session import Session

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

mysql = MySQL(app)

if __name__ == '__main__':
    app.run()

from myapp import routes
from myapp.api import users, login_google