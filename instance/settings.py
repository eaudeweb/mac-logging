# -*- coding: utf-8 -*-

import os

DEBUG = True if os.environ.get('DEBUG', '') in ('True', 'true') else False
SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')

SQLALCHEMY_DATABASE_URI = 'sqlite:///{database}'.format(
  database=os.environ.get('DATABASE', '/var/local/pontaj/files/mac_logging.db')
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

SENTRY_DSN = os.environ.get('SENTRY_DSN', '')
