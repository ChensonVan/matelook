#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

__author__ = 'Changxun Fan'

import sqlite3
import glob
import sys, os, shutil
import time, uuid
import datetime

from config_default import configs


DATA_PATH = configs['DATA_PATH']
DATA_BASE = configs['DATA_BASE']
IMG_DST = configs['IMG_DST']


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


def time_stamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S+0000')


def execute(sql, args):
    """
    :param sql: execute sql
    :return: just execute sql and no return
    """
    conn = None
    try:
        # conn = sqlite3.connect(DATA_BASE)
        conn = sqlite3.connect(DATA_BASE, check_same_thread=False)
        cur = conn.cursor()
        # create tables
        cur.execute(sql, args or ())
        conn.commit()
    except sqlite3.Error as e:
        print("Error from execute: %s" % e.args[0])
        sys.exit(1)
    finally:
        if conn:
            conn.close()


def select(sql, args):
    """
    :param sql:  execute search sql
    :return: return search result, a list contains tuples
    """
    conn = None
    values = None
    try:
        # conn = sqlite3.connect(DATA_BASE)
        conn = sqlite3.connect(DATA_BASE, check_same_thread=False)
        cur = conn.cursor()
        cur.execute(sql, args or ())
        values = cur.fetchall()
        conn.commit()
    except sqlite3.Error as e:
        print("Error from select: %s" % e.args[0])
        sys.exit(1)
    finally:
        if conn:
            conn.close()
    return values


def create_tables():
    """
    :param: None
    :return: None
    """
    create_user_info = """
    create table user_info(zid varchar(10) primary key, full_name varchar(20),
        password varchar(50), birthday varchar(20), email varchar(50),
        home_longitude varchar(20), home_latitude varchar(20), program varchar(20),
        courses varchar(200), mates varchar(1000), image varchar(50), 
        public integer, suspending integer, notifications varchar(500), 
        request varchar(100), description varchar(500), home_suburb varchar(20))
    """

    create_user_post = """
    create table user_post(pid varchar(50) primary key, zid varchar(10) not null, 
        message varchar(500) not null, time varchar(50))
    """

    create_user_comment = """ 
    create table user_comment(cid varchar(50) primary key, pid varchar(50) not null,
        zid varchar(10) not null, message varchar(500) not null, time varchar(50))
    """

    create_notifications = """ 
    create table notifications(nid varchar(50) primary key, 
    from_zid varchar(50) not null, to_zid varchar(50) not null, 
    noti_type varchar(10) not null, time varchar(50), from_name varchar(50),
    from_img varchar(50), pid varchar(50))
    """

    create_requests = """ 
    create table requests(rid varchar(50) primary key, 
    from_zid varchar(50) not null, to_zid varchar(50) not null)
    """

    NEW = False
    try:
        if NEW: execute(create_user_info, ())
        execute('DROP TABLE user_info', ())
    except sqlite3.Error as e:
        print("DROP TABLE user_info: %s" % e.args[0])

    try:
        if NEW: execute(create_user_comment, ())
        execute('DROP TABLE user_comment', ())
    except sqlite3.Error as e:
        print("DROP TABLE user_comment: %s" % e.args[0])

    try:
        if NEW: execute(create_user_post, ())
        execute('DROP TABLE user_post', ())
    except sqlite3.Error as e:
        print("DROP TABLE user_post: %s" % e.args[0])

    try:
        if NEW: execute(create_notifications, ())
        execute('DROP TABLE notifications', ())
    except sqlite3.Error as e:
        print("DROP TABLE notifications: %s" % e.args[0])

    try:
        if NEW: execute(create_requests, ())
        execute('DROP TABLE requests', ())
    except sqlite3.Error as e:
        print("DROP TABLE requests: %s" % e.args[0])
    # print('drop ok')

    execute(create_user_info, ())
    execute(create_user_post, ())
    execute(create_user_comment, ())
    execute(create_notifications, ())
    execute(create_requests, ())
    # print('execute ok')



if __name__ == "__main__":
    test = True
    # create_tables()
    # print('>>> db.py')
    # pid = next_id()
    # # print(pid)
    # print(time_stamp())
    # sql = 'select count(*) from `user_infos`'
    # print(execute(sql, ()))
    # print('>>>')





