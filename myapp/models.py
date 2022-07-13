from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

from app import app

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))

    def get_id(self):
        return self.userid

    def __repr__(self):
        return '<User {}>'.format(self.username)
