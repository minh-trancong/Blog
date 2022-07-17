import MySQLdb.cursors
from flask import jsonify, request, url_for, redirect
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, mysql
from sqlalchemy import delete
from myapp.models import User, db


@app.route('/api/users', methods=['GET'])
def get_all_user():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM `User`")
    result = cursor.fetchall()
    result = {'all_users': [dict(id=i['userid'], email=i['email']) for i in result]}
    return jsonify(result)


@app.route('/api/users/<int:userid>', methods=['GET'])
def get_user(userid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM `User` WHERE userid = %d" % userid)
    result = cursor.fetchone()
    result['password'] = "*****"
    return jsonify(result)


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM User WHERE email = %s', (email,))
    account = cursor.fetchone()
    if account is None:
        return jsonify(message="Incorrect email! Please try again!", category="error", code=401)
    else:
        validate = check_password_hash(account['password'], password)
        if validate is True:
            return jsonify(account=account, message='Logged in successfully!', code=200)
        else:
            return jsonify(message="Incorrect password! Please try again!", category="error", code=401)


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
            return jsonify(message=msg, category='ERROR', code=409)
        else:
            cursor.execute('INSERT INTO User(userid, email, username, password) VALUES (NULL, %s, %s, %s);',
                           (email, username, hashed_password))
            mysql.connection.commit()
            return jsonify(account=dict(username=username, email=email), message='Register Successfully!')
    else:
        msg = 'Don\'t forget to fill in username, password, and email!'
        return jsonify(message=msg, category='ERROR', code=409)


@app.route('/api/delete/users/<int:userid>', methods=['DELETE'])
def delete_user(userid):
    user = User.query.get(userid)
    userinfo = user.get_info()
    db.session.delete(user)
    db.session.commit()
    return jsonify(message="Delete Successfully!", account=userinfo, code=200)


@app.route('/api/update/users/<int:userid>', methods=['PUT'])
def update_information(userid):
    data = request.json
    user = User.query.get(userid)
    if 'occupation' in data:
        user.occupation = data['occupation']
    else:
        return jsonify(message="Not input in {x} field".format(x='occupation'), code=204)
    if 'phone' in data:
        user.phone = data['phone']
    else:
        return jsonify(message="Not input in {x} field".format(x='phone'), code=204)
    if 'lastname' in data:
        user.lastname = data['lastname']
    else:
        return jsonify(message="Not input in {x} field".format(x='lastname'), code=204)
    db.session.commit()
    return jsonify(message="Update successfully", code=200, user=user.get_info())
