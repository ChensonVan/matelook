#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Changxun Fan'

import sqlite3
import glob
import sys, os, shutil
import datetime
import uuid, hashlib
import pickle

from model import User, Post, Comment
from db import *
from config_default import configs


# DATA_PATH = '/import/ravel/3/z5006334/public_html/ass2/dataset-small'
DATA_PATH = configs['DATA_PATH']
DATA_BASE = configs['DATA_BASE']
IMG_DST = configs['IMG_DST']



def init_db():
    """
    init the DATA_BASE, include create all tables and insert the value
    :return: None
    """
    create_tables()

    for usr_path in glob.glob(DATA_PATH + '/*'):
        # print usr_path
        if not os.path.isfile(os.path.join(usr_path, 'user.txt')):
            continue
        with open(os.path.join(usr_path, 'user.txt'), 'r') as file:
            zid = ''
            full_name = ''
            program = ''
            home_longitude = ''
            home_latitude = ''
            courses = ''
            mates = ''
            email = ''
            password = ''
            birthday = ''
            image = 'no_image.png'
            for line in file:
                line = line.strip()
                # users = dict([line.strip().split('=', 1)])
                if line.startswith('zid='):
                    zid = line.split('=')[1]
                if line.startswith('full_name='):
                    full_name = line.split('=')[1]
                if line.startswith('program='):
                    program = line.split('=')[1]
                if line.startswith('home_longitude='):
                    home_longitude = line.split('=')[1]
                if line.startswith('home_latitude='):
                    home_latitude = line.split('=')[1]
                if line.startswith('courses='):
                    courses = line.split('=')[1][1:-1]
                    courses_list = courses.replace(' ', '').split(',')
                    courses = pickle.dumps(courses_list)
                if line.startswith('mates='):
                    mates = line.split('=')[1][1:-1]
                    mates_list = mates.replace(' ', '').split(',')
                    mates = pickle.dumps(mates_list)
                if line.startswith('password='):
                    password = line.split('=')[1]
                if line.startswith('birthday='):
                    birthday = line.split('=')[1]
                if line.startswith('email='):
                    email = line.split('=')[1]
            if os.path.isfile(os.path.join(usr_path, 'profile.jpg')):
                image = zid + '.jpg'
                src = os.path.join(usr_path, 'profile.jpg')
                dst = os.path.join(IMG_DST, image)
                shutil.copy(src, dst)
            # sql = insert_a_user.format(zid, full_name, program, home_longitude,
            #         home_latitude, courses, mates, email, password, birthday,
            #         image)
            # executeDAO(sql)
            # method 1
            zid_password = '%s:%s' % (zid, password)
            sha_password = hashlib.sha1(zid_password.encode('utf-8')).hexdigest()
            # method 2
            # sha1 = hashlib.sha1()
            # sha1.update(zid.encode('utf-8'))
            # sha1.update(b':')
            # sha1.update(password.encode('utf-8'))
            # sha_pwd = sha1.hexdigest()
            user = User(zid=zid, password=sha_password, email=email, full_name=full_name, birthday=birthday, program=program, home_longitude=home_longitude, home_latitude=home_latitude, courses=courses, image=image, mates=mates)
            user.save()

        if not os.path.isdir(os.path.join(usr_path, 'posts')):
            continue
        posts_path = os.path.join(usr_path, 'posts')
        for post in glob.glob(posts_path + '/*'):
            pid = next_id()
            if not os.path.isfile(os.path.join(post, 'post.txt')):
                continue
            with open(os.path.join(post, 'post.txt'), 'r') as file:
                message = ''
                zid = ''
                time = ''
                for line in file:
                    line = line.strip()
                    if line.startswith('message='):
                        message = line.split('=')[1]
                    if line.startswith('from='):
                        zid = line.split('=')[1]
                    if line.startswith('time='):
                        time = line.split('=')[1]
                # message = message.replace("'", "")
                # sql = insert_a_post.format(zid, message, time)
                # executeDAO(sql)
                # pid = insertDAO(sql)
                pid = next_id()
                upost = Post(pid=pid, zid=zid, time=time, message=message)
                upost.save()

            if not os.path.isdir(os.path.join(post, 'comments')):
                continue

            comments_path = os.path.join(post, 'comments')
            for comment in glob.glob(comments_path + '/*'):
                if not os.path.isfile(os.path.join(comment, 'comment.txt')):
                    continue
                with open(os.path.join(comment, 'comment.txt'), 'r') as file:
                    message = ''
                    zid = ''
                    time = ''
                    for line in file:
                        line = line.strip()
                        if line.startswith('message='):
                            message = line.split('=')[1]
                        if line.startswith('from='):
                            zid = line.split('=')[1]
                        if line.startswith('time='):
                            time = line.split('=')[1]
                    # message = message.replace("'", "`")
                    # sql = insert_a_comment.format(pid, zid, message, time)
                    # executeDAO(sql)
                    cid = next_id()
                    ucomment = Comment(cid=cid, pid=pid, zid=zid, time=time, message=message)
                    ucomment.save()



if __name__ == "__main__":
    print(">>> begin init_database \n")
    init_db()
    # r = select('select public, notifications, pendding from `user_info` where `zid`=?', ('z3413158',))
    # print (r)
    print(">>> end init_database")











