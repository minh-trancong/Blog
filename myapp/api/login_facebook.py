import google_auth_oauthlib.flow
import requests
from flask import redirect, session, url_for, request, jsonify
from flask_login import login_user, current_user
from flask_session import Session
from werkzeug.security import generate_password_hash
from myapp.forms import OccupationForm
from app import app
from myapp.models import User, db


@app.route('/api/facebook/register', methods=['GET', 'POST'])
def fb_login():
    body = request.json
    input_token = body['input_token']
    access_token = body['access_token']
    data = requests.get('https://graph.facebook.com/debug_token?input_token={input_token}&access_token={access_token}'.format(input_token=input_token, access_token=access_token)).json()
    if 'user_id' in data['data']:
        uinfo = requests.get('https://graph.facebook.com/v14.0/{user_id}?fields=email,name,last_name,first_name&access_token={access_token}'.format(
            user_id=data['data']['user_id'], access_token=input_token)).json()
        user = User.query.filter_by(email=uinfo['email']).first()
        print(user)
        if user:
            login_user(user)
            return jsonify(message="Login successfully", account=user.get_info())
        else:
            # Register
            username = uinfo['email'].split('@')[0]
            user = User(firstname=uinfo['first_name'], lastname=uinfo['last_name'], email=uinfo['email'],
                        password='NoPassword', username=username)
            db.session.add(user)
            db.session.commit()
            return jsonify(message="Register successfully", account=user.get_info())
    else:
        return data

