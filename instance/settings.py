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
