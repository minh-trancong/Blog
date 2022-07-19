import datetime

from flask import jsonify, request

from app import app
from myapp.models import db, Post


@app.route('/api/users/<int:id>/posts')
def get_user_post(id):
    post = Post.query.filter_by(userid=id).all()
    post_export = {}
    for i in range(len(post)):
        info = post[i].get_info()
        post_export[i + 1] = info
        if len(info['body']) > 100:
            dots = "..."
        else:
            dots = ""
        post_export[i + 1]['body'] = info['body'][:100] + dots
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


@app.route('/api/posts/<int:id>', methods=['GET', 'DELETE'])
def get_post(id):
    post = Post.query.get(id)
    if post:
        if request.method == 'GET':
            return jsonify(post=post.get_info(), message="Successfully")
        elif request.method == 'DELETE':
            db.session.delete(post)
            db.session.commit()
            return jsonify(post=post.get_info(), message="DELETE successfully")
    else:
        return jsonify(message="No posts founded", code=404)


@app.route('/api/posts/page=<int:pageid>', methods=['GET'])
def get_all_posts(pageid):
    post = Post.query.paginate(pageid, 10, False)
    p_ex = {}
    i = 0
    for p in post.items:
        p_ex[i] = p.get_info()
        if len(p.get_info()['body']) > 100:
            p_ex[i]['body'] = p.get_info()['body'][:100] + "..."
        i = i + 1
    return jsonify(posts=p_ex)

