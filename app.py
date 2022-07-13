from authlib.integrations.flask_client import OAuth
from flask import Flask
from flask_mysqldb import MySQL

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)

if __name__ == '__main__':
    app.run()

from myapp import routes
from myapp.api import users