import requests
from flask import render_template, session, redirect, url_for, request
from flask_login import LoginManager, login_required, login_user, logout_user

from app import app
from myapp.forms import LoginForm, RegisterForm
from myapp.models import User
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@app.route('/')
def index():
    return render_template('index.html', start_link='/login')


@app.route('/home')
@login_required
def home():
    result = requests.get(url_for('get_user', userid=session['id'], _external=True)).json()
    username = result["username"]
    return render_template('home.html', username=username)


@login_manager.unauthorized_handler
def unauthorized():
    return render_template('notloggedin.html')


@app.route("/login", methods=['GET', 'POST'])
def login_form():
    form = LoginForm()
    msg = ""
    if request.method == 'POST':
        body = dict(email=form.email.data, password=form.password.data)
        result = requests.post(url_for('login', _external=True), json=body).json()
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
    result = requests.post(url_for('register', _external=True), json=body).json()
    msg = result["message"]
    if form.email.data is None or form.password.data is None:
        msg = ""  # Khi load form login lần đầu, sẽ không hiện error
    return render_template('register.html', RegisterForm=form, message=msg)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
