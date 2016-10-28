#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

__author__ = 'Changxun Fan'
from db import *
from model import User, Post, Comment, Pagination, Notifications, Requests
import operator
import pickle


# com = Comment.findByKey('001477622858155e541cf25963d4993b02d4fc9a7a6a8d3000')
# print(dir(com))


sql = "SELECT `name` FROM `sqlite_temp_master` WHERE type='table' AND name=`user_info` or name=`user_post`"
print(select(sql, ()))















