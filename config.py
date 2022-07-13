import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://minh:123@localhost/blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # App
    SECRET_KEY = 'my-secret'

    # Đăng nhập bằng Google
    GOOGLE_CLIENT_ID = "811649600099-vam2ntbjisad228kaa8atma7kbenacqe.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "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"
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

    # MYSQL Config
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'minh'
    MYSQL_PASSWORD = '123'
    MYSQL_DB = 'blog'



def url(path):
    host_link = 'http://127.0.0.1:5000'
    return host_link + path
