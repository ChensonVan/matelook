# config_default.py
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

DB_SIZE = 'large'


configs = {
    'DATA_PATH' : DIR_PATH + '/static/dataset/dataset-large',
    'DATA_BASE' : DIR_PATH + '/matelook.db',
    'IMG_DST' : DIR_PATH  +'/static/profile',
    'URL' : '127.0.0.1',
    'PORT' : '8088',
    'LIMIT' : 5
}

