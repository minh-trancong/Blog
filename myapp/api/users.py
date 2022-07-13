import MySQLdb.cursors
from flask import jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, mysql


@app.route('/api/users/<int:userid>', methods=['GET'])
def get_user(userid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM `User` WHERE userid = %d" % userid)
    result = cursor.fetchone()
    result['password'] = "*****"
    return jsonify(result)


@app.route('/api/login', methods=['POST'])
def get_login():
    data = request.json
    email = data['email']
    password = data['password']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM User WHERE email = %s', (email,))
    account = cursor.fetchone()
    if account is None:
        return jsonify(message="Incorrect email! Please try again!", category="error", status=401)
    else:
        validate = check_password_hash(account['password'], password)
        if validate is True:
            return jsonify(account)
        else:
            return jsonify(message="Incorrect password! Please try again!", category="error", status=401)


@app.route('/api/register', methods=['GET', 'POST'])
def register():
    data = request.json
    email = data['email']
    username = data['username']
    password = data['password']
    # Kiểm tra xem đã có email hoặc username trong database chưa
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if email and username and password:
        hashed_password = generate_password_hash(password)
        cursor.execute('SELECT * FROM User WHERE email = %s OR username = %s', (email, username))
        account = cursor.fetchone()
        if account:
            msg = ""
            if account['email'] == email:
                msg = 'Email already exists!'
            elif account['username'] == username:
                msg = 'Username already exists!'
            return jsonify(message=msg, category='ERROR', status=409)
        else:
            cursor.execute('INSERT INTO User(userid, email, username, password) VALUES (NULL, %s, %s, %s);',
                           (email, username, hashed_password))
            mysql.connection.commit()
            return jsonify(account=dict(username=username, email=email), message='Register Successfully!')
    else:
        msg = 'Don\'t forget to fill in username, password, and email!'
        return jsonify(message=msg, category='ERROR', status=409)
