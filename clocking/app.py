# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from flask import Flask

from .api import api
from .models import db

DEFAULT_CONFIG = {}


def create_app(config={}):
    app = Flask(__name__, instance_relative_config=True)
    app.config.update(DEFAULT_CONFIG)
    if not config:
        app.config.from_pyfile('settings.py', silent=True)
    else:
        app.config.update(config)
    db.init_app(app)
    app.register_blueprint(api)
    if app.config.get('SENTRY_DSN'):
        from raven.contrib.flask import Sentry
        Sentry(app)

    return app

app = create_app()

@app.context_processor
def utility_processor():
    def get_enddate(enddate):
        enddate += timedelta(hours=8)
        if enddate < datetime.now():
            return enddate.strftime('%H:%M')
        else:
            return '-'
    return dict(get_enddate=get_enddate)


@app.route('/crashme')
def crashme():
    raise RuntimeError("Crashing as requested by you")
