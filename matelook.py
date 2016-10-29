#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

__author__ = 'Changxun Fan'

from flask import *
from functools import wraps
from model import User, Post, Comment, Pagination, Notifications, Requests
from mail import MailUtils
from db import next_id, select, time_stamp
from config_default import configs
import re, hashlib, pickle
import datetime, time

_URL_ = configs['URL']
_PORT_ = configs['PORT']



app = Flask(__name__)
app.secret_key = 'this is random string'

_RE_EMAIL_ = re.compile('^z[0-9]{7}$')


def login_required(function_to_wrap):
    @wraps(function_to_wrap)
    def wrap(*args, **kwargs):
        if "zid" in session:
            return function_to_wrap(*args, **kwargs)
        else:
            flash("Please Login To Continue.")
            return redirect(url_for("login"))
    return wrap


@app.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    # if session.get('zid') == None:
    #     return redirect(url_for('login'))
    zid = session['zid']
    user = User.findByKey(zid)
    page = int(request.args.get('page', '1'))
    recentPosts = user.getRecentPosts()
    total = len(recentPosts)
    pag = Pagination(page, total)
    return render_template('home.html', user=user, pag=pag)


@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    zid = request.form.get('zid')
    password = request.form.get('password')
    if not _RE_EMAIL_.match(zid):
        flash('Login Failed: zid was wrong!')
        return render_template('login.html')

    user = User.findByKey(zid)
    if not user:
        flash('Login Failed: zid doesn\'t exist!')
        return render_template('login.html')
    if not password:
        flash('password was wrong!')
        return render_template('login.html')

    sha1 = hashlib.sha1()
    sha1.update(zid.encode('utf-8'))
    sha1.update(b':')
    sha1.update(password.encode('utf-8'))
    sha_password = sha1.hexdigest()
    if sha_password != user.password:
        flash('password was wrong!')
        return render_template('login.html')

    session['zid'] = zid
    session['password'] = sha_password
    return redirect(url_for('home'))


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    if 'zid' in session:
        session.pop('zid')
    if 'password' in session:
        session.pop('password')
    flash('You have been logged out.')
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    zid = request.form.get('zid', '')
    password = request.form.get('password', '')
    email = request.form.get('email', '')

    if not _RE_EMAIL_.match(zid):
        flash('Register Failed: zid was wrong.')
        return render_template('register.html')

    if not password:
        flash('Register Failed: password cannot be empty.')
        return render_template('register.html')

    user = User.findByKey(zid)
    if user:
        flash('Register Failed: zid is already in use.')
        return render_template('register.html')

    zid_password = '%s:%s' % (zid, password)
    sha_password = hashlib.sha1(zid_password.encode('utf-8')).hexdigest()
    user = User(zid=zid, password=sha_password, email=email)
    user.save()

    flash('Register Success: you can login now.')
    return redirect(url_for('login'))


@app.route('/matelook', methods=['POST', 'GET'])
@login_required
def matelook():
    u_zid = request.args.get('u_zid')
    mate = User.findByKey(u_zid)
    zid = session['zid']
    user = User.findByKey(zid)
    if not mate:
        flash('User ' + u_zid + ' not found!')
    return render_template('matelook.html', user=user, mate=mate)


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    zid = session['zid']
    password = session['password']
    user = User.findByKey(zid)
    if request.method == 'GET':
        return render_template('profile.html', user=user)
    new_password = request.form.get('password')
    old_password = request.form.get('old_password')
    if old_password:
        zid_password = '%s:%s' % (zid, old_password)
        sha_password = hashlib.sha1(zid_password.encode('utf-8')).hexdigest()
        if sha_password != user.password:
            flash('Old password was wrong!')
            return render_template('profile.html', user=user)

    description = request.form.get('description', '')
    full_name = request.form.get('full_name', '')
    email = request.form.get('email', '')
    birthday = request.form.get('birthday', '')
    program = request.form.get('program', '')
    courses = request.form.get('courses', '')
    home_latitude = request.form.get('home_latitude', '')
    home_longitude = request.form.get('home_longitude', '')
    home_suburb = request.form.get('home_suburb', '')
    public = int(request.form.get('public'))

    if new_password:
        zid_password = '%s:%s' % (zid, new_password)
        sha_password = hashlib.sha1(zid_password.encode('utf-8')).hexdigest()
        user.password = sha_password
    if description:
        user.description = description
    if full_name:
        user.full_name = full_name
    if email:
        user.email = email
    if birthday:
        user.birthday = birthday
    if program:
        user.program = program
    # if courses:
    #     user.courses = courses
    if home_latitude:
        user.home_latitude = home_latitude
    if home_longitude:
        user.home_longitude = home_longitude
    if home_suburb:
        user.home_suburb = home_suburb
    user.public = public
    user.update()
    flash('Success: you have change your infomation.')
    return render_template('profile.html', user=user)


@app.route('/search', methods=['POST', 'GET'])
@app.route('/search/<action>', methods=['POST', 'GET'])
@login_required
def search(action=None):
    zid = session['zid']
    user = User.findByKey(zid)
    page = int(request.args.get('page', '1'))
    total = len(user.mateSuggestions())
    pag = Pagination(page, total)
    if action == 'user':
        query = request.args.get('query', '')
        users = User.findByName(query)
        total = len(users)
        pag = Pagination(page, total)
        return render_template('search.html', user=user, users=users, query=query, pag=pag)
    if action == 'post':
        query = request.args.get('query', '')
        posts = Post.findPosts('message', query)
        total = len(posts)
        pag = Pagination(page, total)
        return render_template('home.html', user=user, posts=posts, query=query, pag=pag)
    return render_template('search.html', user=user, pag=pag)


@app.route('/account/<action>', methods=['POST', 'GET'])
def account(action):
    if action == 'recovery':
        if request.method == 'GET':
            return render_template('recovery.html')
        if request.method == 'POST':
            zid = request.form.get('zid', '')
            email = request.form.get('email', '')
            # validate zid and email
            user = User.findByKey(zid)
            if not user:
                flash('Failed: zid doesn\'exist.')
                return render_template('recovery.html')
            # if email != user.email:
            #     flash('Failed: email was wrong.')
            #     return render_template('recovery.html')
            mail = MailUtils(email, 'MateLook Team', user.full_name)
            resetCode = next_id()
            mail.reset(zid, resetCode)
            flash('Success: vaildate email has send, pleacse check your inbox.')
            return render_template('login.html')
    if action == 'reset':
        zid = request.args.get('zid', '')
        resetCode = request.args.get('resetCode', '')
        # validate zid and resetCode
        if resetCode and zid:
            user = User.findByKey(zid)
            if not user:
                flash('Failed: zid doesn\'exist.')
                return render_template('recovery.html')
        return render_template('recovery.html', user=user)
    if action == 'resetSave':
        zid = request.form.get('zid', '')
        password = request.form.get('password', '')
        password_check = request.form.get('password_check')
        user = User.findByKey(zid)
        if password != password_check:
            flash('Failed: password doesn\'t consist.')
            return render_template('recovery.html', user=user)
        if user:
            zid_password = '%s:%s' % (zid, password)
            sha_password = hashlib.sha1(zid_password.encode('utf-8')).hexdigest()
            user.password = sha_password
            user.update()
            return redirect(url_for('login'))
    return redirect(url_for('login'))


@app.route('/post', methods=['POST'])
@login_required
def post():
    zid = session['zid']
    if not zid:
        return redirect(url_for('login'))
    message = request.form.get('post')
    new_post = Post(zid=zid, message=message)
    new_post.save()
    flash('Success: you have post a new psot.')
    return redirect(url_for('home'))


@app.route('/postlook', methods=['POST', 'GET'])
@login_required
def postlook():
    zid = session['zid']
    user = User.findByKey(zid)
    pid = request.args.get('pid')
    post = Post.findByKey(pid)
    poster = User.findByKey(post.zid)
    page = int(request.args.get('page', '1'))
    total = len(post.getComments())
    pag = Pagination(page, total)

    return render_template('postlook.html', post=post, user=user, poster=poster, pag=pag)


@app.route('/comment', methods=['POST'])
@login_required
def comment():
    zid = session['zid']
    user = User.findByKey(zid)
    if not user:
        return redirect(url_for('login'))
    pid = request.form.get('pid')
    poster_zid = request.form.get('poster_zid')
    message = request.form.get('message')
    new_comment = Comment(pid=pid, zid=zid, message=message)
    new_comment.save()
    flash('Success: you have post a new comment.')
    notification = Notifications(from_zid=user.zid, to_zid=poster_zid, noti_type='reply', from_name=user.full_name, from_img=user.image, pid=pid)
    # notification.pid = pid
    notification.save()
    post = Post.findByKey(pid)
    poster = User.findByKey(post.zid)
    page = int(request.args.get('page', '1'))
    total = len(post.getComments())
    pag = Pagination(page, total)
    return redirect(url_for('postlook', pid=pid, page=page))


@app.route('/notifications', methods=['POST', 'GET'])
@login_required
def notifications():
    zid = session['zid']
    user = User.findByKey(zid)
    action = request.form.get('action', '')
    nid = request.form.get('nid', '')
    if action == 'accept':
        n = user.getNotificationById(nid)
        # add new notifications to sender
        notification = Notifications(from_zid=user.zid, to_zid=n.from_zid, noti_type='accept', from_name=user.full_name, from_img=user.image)
        notification.save()
        # delete this request from table
        user_request = Requests.getRequest(n.from_zid, n.to_zid)
        user_request.remove()
        # add to matelist at both sides
        user.mate(n.from_zid)
        # remove this notification
        user.removeNotificationById(n.nid)
    elif action == 'decline':
        n = user.getNotificationById(nid)
        # add new notifications to sender
        notification = Notifications(from_zid=user.zid, to_zid=n.from_zid, noti_type='decline', from_name=user.full_name, from_img=user.image)
        notification.save()
        # delete this request from table
        user_request = Requests.getRequest(n.from_zid, n.to_zid)
        user_request.remove()
        # remove this notification
        user.removeNotificationById(n.nid)
    # look mate page
    elif action == 'look':
        n = user.getNotificationById(nid)
        user.removeNotificationById(n.nid)
        return redirect(url_for('matelook', u_zid=n.from_zid))
    # read post / comments
    elif action == 'read':
        n = user.getNotificationById(nid)
        user.removeNotificationById(n.nid)
        return redirect(url_for('postlook', pid=n.pid))
    elif action == 'ignore':
        n = user.getNotificationById(nid)
        user.removeNotificationById(n.nid)

    user.clearNotice()
    isNotifications = len(user.getNotifications()) - 1
    page = int(request.args.get('page', '1'))
    notifications = user.getNotifications()
    total = len(notifications) - 1
    pag = Pagination(page, total)
    return render_template('notifications.html', user=user, notifications=user.getNotifications(), pag=pag, isNotifications=isNotifications)


@app.route('/myposts', methods=['POST', 'GET'])
@login_required
def myposts():
    zid = session['zid']
    user = User.findByKey(zid)
    page = int(request.args.get('page', '1'))
    action = request.args.get('action', '')
    if action:
        pid = request.args.get('pid', '')
        d_post = Post.findByKey(pid)
        d_post.removeComments()
        d_post.remove()
    myposts = user.getPosts()
    total = len(myposts) - 1
    pag = Pagination(page, total)
    return render_template('home.html', user=user, myposts=myposts, pag=pag, print_myposts=True)


@app.route('/mateManager', methods=['POST', 'GET'])
@login_required
def mateManager():
    zid = session['zid']
    user = User.findByKey(zid)
    action = request.form.get('action', '')
    if action == 'delete':
        m_zid = request.form.get('m_zid', '')
        # delete at both sides
        user.unmate(m_zid)

        notification = Notifications(from_zid=user.zid, to_zid=m_zid, noti_type='delete', from_name=user.full_name, from_img=user.image)
        notification.save()
    elif action == 'add':
        m_zid = request.form.get('m_zid', '')
        # add to requests table
        mate_request = Requests(from_zid=zid, to_zid=m_zid)
        mate_request.save()
        notification = Notifications(from_zid=user.zid, to_zid=m_zid, noti_type='add', from_name=user.full_name, from_img=user.image)
        notification.save()
    query = request.form.get('query', '')
    page = int(request.form.get('page', '1'))
    suggestion = request.form.get('suggestion', '')
    if suggestion:
        return redirect(url_for('search', page=page))
    return redirect(url_for('search', action='user', query=query, page=page))


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
#
#
# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500


if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # app.run(host=_URL_, port=_PORT_)
    app.run(port=8080)
    # debug=True, user_reloader=True
