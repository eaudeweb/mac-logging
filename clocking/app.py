from datetime import datetime, timedelta

from flask import Flask, url_for
from flask_admin import Admin, helpers as admin_helpers
from flask_security import Security, SQLAlchemyUserDatastore

from .api import api, view
from .models import db, Person, Address, Entry, User, Role

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


admin = Admin(app,
              name='Clocking',
              base_template='my_master.html',
              template_mode='bootstrap3')

admin.add_view(view.ProtectedModelView(Role, db.session))
admin.add_view(view.ProtectedModelView(User, db.session))
admin.add_view(view.ProtectedModelView(Person, db.session))
admin.add_view(view.ProtectedModelView(Address, db.session))
admin.add_view(view.ProtectedModelView(Entry, db.session))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


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
