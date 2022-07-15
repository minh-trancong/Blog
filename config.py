import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://minh:123@localhost/blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # App
    SECRET_KEY = 'my-secret'

    # MYSQL Config
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'minh'
    MYSQL_PASSWORD = '123'
    MYSQL_DB = 'blog'



