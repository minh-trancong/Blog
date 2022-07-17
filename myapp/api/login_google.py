import google_auth_oauthlib.flow
import requests
from flask import redirect, session, url_for, request, jsonify
from flask_login import login_user, current_user
from flask_session import Session
from werkzeug.security import generate_password_hash
from myapp.forms import OccupationForm

from app import app
from myapp.models import User, db
Session(app)
# Các keys để dùng API trong file 'client_secret.json'
CLIENT_SECRETS_FILE = "client_secret.json"

SCOPES = ['openid https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email']
API_SERVICE_NAME = 'google_login'
API_VERSION = 'v1'
access_token_link = 'https://www.googleapis.com/oauth2/v1/userinfo?access_token='


# Body: google access_token
# Return: User info in database
@app.route('/api/google/login', methods=['POST', 'GET'])
def google_login():
    data = request.json
    token = data['token']
    userinfo = requests.get(access_token_link + token).json()
    user = User.query.filter_by(email=userinfo['email']).first()
    if user:
        login_user(user)
        return jsonify(account=user.get_info(), message='Logged in successfully!', code=200)
    else:
        return jsonify(message='Account has not been registered in system!', code=401)


# Body: google access_token
# Return: redirect to input occupation
@app.route('/api/google/register', methods=['GET', 'POST'])
def google_register():
    token = request.json['token']
    userinfo = requests.get(access_token_link + token).json()
    user = User.query.filter_by(email=userinfo['email']).first()
    if user:
        return jsonify(account=user.get_info(), message='Can not registered! Account already exists', code=409)
    else:
        data = request.json
        email = userinfo['email']
        username = email.split('@')[0]
        lastname = None
        firstname = None
        if 'family_name' in userinfo:
            lastname = userinfo['family_name']
        if 'given_name' in userinfo:
            firstname = userinfo['given_name']
        user = User(username=username, email=email, firstname=firstname, lastname=lastname, password="NoPassword")
        db.session.add(user)
        db.session.commit()
        session['registered_id'] = user.get_id()
        url = url_for('google_post_occupation', userid=user.get_id())
        return jsonify(account=user.get_info(), redirect_url_api=url, message="Registered successfully!")


# Body: occupation
# Return: userinfo
@app.route('/api/google/<int:userid>/occupation', methods=['GET', 'POST'])
def google_post_occupation(userid):
    data = request.json
    occupation = None
    if 'occupation' in data:
        occupation = data['occupation']
    user = User.query.get(userid)
    user.occupation = occupation
    db.session.commit()
    return jsonify(account=user.get_info(), message='Registered Successfully!', code=201)


@app.route('/api/google/checkmail')
def check_google_email():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('google_oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent',  # để khi logout có thể đăng nhập lại
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)


@app.route('/api/google/callback')
def google_oauth2callback():
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('google_oauth2callback', _external=True)
    authorization_response = request.url
    token = flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)
    res = requests.post(url_for('google_login', _external=True), json=dict(token=token['access_token'])).json()
    if res['code'] == 200:
        user = User.query.get(res['account']['userid'])
        login_user(user)
        return redirect(url_for('home', _external=True))
    else:
        data = requests.post(url_for('google_register', _external=True), json=dict(token=token['access_token'])).json()
        id = data['account']['userid']
        return redirect(url_for('post_occupation', id=id, _external=True))


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}