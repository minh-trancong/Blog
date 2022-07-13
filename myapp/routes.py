import requests
from flask import render_template, session, redirect, url_for, request
from flask_login import LoginManager, login_required, login_user, UserMixin, logout_user
from flask_sqlalchemy import SQLAlchemy

from app import app
from config import url
from myapp.forms import LoginForm, RegisterForm

login_manager = LoginManager()
login_manager.init_app(app)
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


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@app.route('/')
def index():
    return render_template('index.html', start_link='/login')


@app.route('/home')
@login_required
def home():
    result = requests.get(url('/api/users/' + str(session["id"]))).json()
    username = result["username"]
    return render_template('home.html', username=username)


@login_manager.unauthorized_handler
def unauthorized():
    return render_template('notloggedin.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    msg = ""
    if request.method == 'POST':
        body = dict(email=form.email.data, password=form.password.data)
        result = requests.post(url('/api/login'), json=body).json()
        if result["status"] == 401:
            if form.email.data is None or form.password.data is None:
                msg = ""  # Khi load form login lần đầu, sẽ không hiện error
            else:
                msg = result["message"]
        else:
            session['loggedin'] = True
            session['id'] = result['userid']
            user = User.query.get(result['userid'])
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', LoginForm=form, message=msg)


@app.route("/register", methods=["GET", "POST"])
def register_form():
    form = RegisterForm()
    body = dict(email=form.email.data, password=form.password.data, username=form.username.data)
    result = requests.post(url('/api/register'), json=body).json()
    msg = result["message"]
    if form.email.data is None or form.password.data is None:
        msg = ""  # Khi load form login lần đầu, sẽ không hiện error
    return render_template('register.html', RegisterForm=form, message=msg)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
