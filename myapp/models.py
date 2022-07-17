from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

from app import app

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True)
    email = db.Column(db.String(255), index=True, unique=True)
    password = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    occupation = db.Column(db.String(255))

    def get_id(self):
        return self.userid

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_info(self):
        return dict(userid=self.userid, username=self.username, email=self.email, password=self.password,
                    firstname=self.firstname, lastname=self.lastname, occupation=self.occupation)
