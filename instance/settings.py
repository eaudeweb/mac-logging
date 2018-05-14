# -*- coding: utf-8 -*-

import os

DEBUG = True if os.environ.get('DEBUG', '') in ('True', 'true') else False
SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')

SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}'.format(
    os.environ.get('DATABASES_USER'), os.environ.get('DATABASES_PASSWORD'),
    os.environ.get('DATABASES_HOST'))

SENTRY_DSN = os.environ.get('SENTRY_DSN', '')

REPORT_DIR = (os.path.dirname(os.path.dirname(__file__))) + '/files/'

REPORT_FILE = 'Report.xlsx'

# Flask-Security config
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/"
SECURITY_POST_LOGOUT_VIEW = "/"
SECURITY_POST_REGISTER_VIEW = "/"

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = '********'
MAIL_PASSWORD = '********'
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# Flask-Security features
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = False
SECURITY_SEND_REGISTER_EMAIL = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
