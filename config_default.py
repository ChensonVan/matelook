#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

__author__ = 'Changxun Fan'
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

DB_SIZE = ['small', 'medium', 'large']


configs = {
    'DATA_PATH' : DIR_PATH + '/static/dataset/dataset-' + DB_SIZE[1],
    'DATA_BASE' : DIR_PATH + '/matelook.db',
    'IMG_DST' : DIR_PATH  +'/static/profile',
    'URL' : '0.0.0.0',
    'PORT' : '3487',
    'LIMIT' : 5
}

