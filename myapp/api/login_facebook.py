import google_auth_oauthlib.flow
import requests
from flask import redirect, session, url_for, request, jsonify
from flask_login import login_user, current_user
from flask_session import Session
from werkzeug.security import generate_password_hash
from myapp.forms import OccupationForm
from app import app
from myapp.models import User, db


@app.route('/api/facebook/login')
def fb_login():
    body = request.json
    input_token = body['input_token']
    access_token = body['access_token']
    data = requests.get('graph.facebook.com/debug_token?input_token={input_token}&access_token={access_token}'.format(input_token=input_token, access_token=access_token)).json()
    if data['is_valid']:
        return jsonify(msg="ok", data=data)
    else:
        return jsonify(msg="Not ok", data=data)