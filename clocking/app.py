from datetime import datetime, timedelta

from flask import Flask, url_for
from flask_admin import helpers as admin_helpers
from flask_login import LoginManager
from flask_mail import Mail
from flask_security import Security, SQLAlchemyUserDatastore

from .api import api, view
from .models import db, User, Role
from .admin import admin

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
    admin.init_app(app)
    if app.config.get('SENTRY_DSN'):
        from raven.contrib.flask import Sentry
        Sentry(app)

    return app


app = create_app()

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
mail = Mail(app)


@app.before_first_request
def before_first_request():
    user_datastore.find_or_create_role(name='superuser')
    user_datastore.find_or_create_role(name='user')
    # encrypted_password = utils.encrypt_password('password')
    # if not user_datastore.get_user('admin@email.com'):
    #     user_datastore.create_user(email='admin@email.com', password=encrypted_password)
    # db.session.commit()
    # user_datastore.add_role_to_user('admin@email.com', 'superuser')
    db.session.commit()


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


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
