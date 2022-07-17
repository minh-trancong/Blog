import MySQLdb.cursors
from flask import jsonify, request, url_for, redirect
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from app import app, mysql
from sqlalchemy import delete
from myapp.models import User, db, Post


@app.route('/api/users/<int:id>/posts')
def get_post(id):
    post = Post.query.filter_by(userid=id).all()
    post_export = {}
    for i in range(len(post)):
        post_export[i+1] = post[i].get_info()
    return jsonify(post_count=len(post), post_details=post_export)


@app.route('/api/users/<int:id>/posts/create', methods=['POST'])
def post_create(id):
    data = request.json
    # db.session.rollback()
    if 'title' in data:
        title = data['title']
    else:
        return jsonify(message="Not input in {x} field".format(x='title'), code=204)
    if 'body' in data:
        body = data['body']
    else:
        return jsonify(message="Not input in {x} field".format(x='body'), code=204)
    post = Post(title=title, body=body, userid=id, timestamp=datetime.datetime.now())
    db.session.add(post)
    db.session.commit()
    return jsonify(post=post.get_info(), message="Create a post successfully", code=200)