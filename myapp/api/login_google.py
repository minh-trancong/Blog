import google_auth_oauthlib.flow
import requests
from flask import redirect, session, url_for, request
from flask_login import login_user

from app import app
from myapp.models import User, db

# Các keys để dùng API trong file 'client_secret.json'
CLIENT_SECRETS_FILE = "client_secret.json"

SCOPES = ['openid https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email']
API_SERVICE_NAME = 'google_login'
API_VERSION = 'v1'


@app.route('/login/google')
def login_google():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('google_oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)


@app.route('/login/google/authorize')
def google_oauth2callback():
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('google_oauth2callback', _external=True)
    authorization_response = request.url
    token = flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)
    userinfo = requests.get(
        'https://www.googleapis.com/oauth2/v1/userinfo?access_token=' + token['access_token']).json()
    user = User.query.filter_by(email=userinfo['email']).first()
    if user:
        login_user(user)
        return redirect(url_for('home'))
    else:
        email = userinfo['email']
        username = email.split('@')[0]
        user = User(username=username, email=email, firstname=userinfo['given_name'], lastname=userinfo['family_name'],
                    password='NotInput')
        # todo Cần thêm tính năng nhập mật khẩu cho người dùng Google
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
