import os
from datetime import timedelta

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = '12345678'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'fangyi'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False

# session 过期时间
PERMANENT_SESSION_LIFETIME = timedelta(days=1)

SECRET_KEY = os.urandom(24)
