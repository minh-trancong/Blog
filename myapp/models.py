from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

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
    phone = db.Column(db.String(255))

    def get_id(self):
        return self.userid

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_info(self):
        return dict(userid=self.userid, username=self.username, email=self.email, password=self.password,
                    firstname=self.firstname, lastname=self.lastname, occupation=self.occupation, phone=self.phone)

    def get_name(self):
        if self.firstname and self.lastname:
            return self.firstname + " " + self.lastname
        elif self.firstname:
            return self.firstname
        else:
            return self.lastname

class Post(UserMixin, db.Model):
    postid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), index=True)
    body = db.Column(db.String(8000), index=True)
    userid = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    def get_id(self):
        return self.postid

    def __repr__(self):
        return '<Post {}>'.format(self.title)

    def get_info(self):
        return dict(postid=self.postid, title=self.title, body=self.body, userid=self.userid, timestamp=self.timestamp)


class React(UserMixin, db.Model):
    postid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, primary_key=True)

    def get_id(self):
        return dict(postid=self.postid, userid=self.userid)

    def __repr__(self):
        return '<React %d - %d>'.format(self.postid, self.userid)
