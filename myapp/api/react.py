import datetime

from flask import jsonify, request, url_for
import requests
from app import app
from myapp.models import db, Post, React, User


@app.route('/api/reacts/users/<int:userid>/posts/<int:postid>', methods=['GET', 'POST', 'DELETE'])
def do_react(postid, userid):
    # db.session.rollback()
    react = React.query.get(dict(postid=postid, userid=userid))
    post_details = requests.get(url_for('get_post', id=postid, _external=True)).json()
    body = post_details['post']['body']
    x = "..." if len(body) > 100 else ""
    post_details['post']['body'] = body[:100] + x
    if react:
        if request.method == 'GET':
            return jsonify(reactid=react.get_id(), user_info=User.query.get(userid).get_info(), post_details=post_details)
        if request.method == 'DELETE':
            db.session.delete(react)
            db.session.commit()
            return jsonify(reactid=react.get_id(), user_info=User.query.get(userid).get_info(), post_details=post_details)
        if request.method == 'POST':
            return jsonify(message="Already Exists!", reactid=react.get_id())
    else:
        if request.method == 'POST':
            react = React(userid=userid, postid=postid)
            db.session.add(react)
            db.session.commit()
            print(react.get_id(), " --- ", post_details)
            return jsonify(reactid=react.get_id(), user_info=User.query.get(userid).get_info(), post_details=post_details)
        return jsonify(code=404, message="NOT EXISTS userid or postid. Check again!")


@app.route('/api/reacts', methods=['GET'])
def get_all_reacts():
    react = React.query.all()
    react_exp = {}
    for i in range(len(react)):
        react_exp[i+1] = react[i].get_id()
    return jsonify(react=react_exp)


@app.route('/api/reacts/posts/<int:postid>', methods=['GET'])
def get_post_reacts(postid):
    react = React.query.filter_by(postid=postid).all()
    react_exp = {}
    for i in range(len(react)):
        react_exp[i + 1] = react[i].get_id()
    if len(react) == 0:
        return jsonify(message="NO reacts founded", code=404)
    elif len(react) == 1:
        react1 = react[-1]
        user1 = User.query.get(react1.get_id()['userid'])
        return jsonify(react=react_exp, likes=user1.get_name(), _url_likes=url_for('get_likes_details', postid=postid, _external=True))
    else:
        react1 = react[-1]
        react2 = react[-2]
        user1 = User.query.get(react1.get_id()['userid'])
        user2 = User.query.get(react2.get_id()['userid'])
        msg = dict(user1=user1.get_name(), user2=user2.get_name(), userleft=len(react)-2)
        if msg['userleft'] == 0:
            return jsonify(likes="{a} and {b} liked this post".format(a=msg['user1'], b=msg['user2']),react_count=len(react), react=react_exp, _url_likes=url_for('get_likes_details', postid=postid, _external=True))
        if msg['userleft'] == 1:
            return jsonify(likes="{a}, {b}, and {n} other person liked this post".format(a=msg['user1'], b=msg['user2'], n=msg['userleft']),react_count=len(react), react=react_exp, _url_likes=url_for('get_likes_details', postid=postid, _external=True))
        else:
            return jsonify(likes="{a}, {b} and {n} other people liked this post".format(a=msg['user1'], b=msg['user2'],n=msg['userleft']), react_count=len(react), react=react_exp, _url_likes=url_for('get_likes_details', postid=postid, _external=True))


@app.route('/api/reacts/posts/<int:postid>/likes', methods=['GET'])
def get_likes_details(postid):
    react = React.query.filter_by(postid=postid).all()
    if len(react) == 0:
        return jsonify(message="NO reacts founded", code=404)
    else:
        user = {}
        i = 0
        for r in react:
            user[i] = User.query.get(r.get_id()['userid']).get_name()
            i = i + 1
        return jsonify(likes=user)
