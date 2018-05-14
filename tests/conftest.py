from flask import render_template
from flask_security import login_required
from flask_webtest import TestApp
from flask_login import LoginManager
from flask_security import Security, SQLAlchemyUserDatastore
from pytest import fixture
from clocking.models import db, User, Role


from clocking.models import db
from clocking.app import create_app

TEST_CONFIG = {
    'DEBUG': True,
    'SERVER_NAME': 'noname',
    'SECRET_KEY': 'secret',
    'LOGIN_DISABLED': False,
    'WTF_CSRF_ENABLED': False,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SECURITY_URL_PREFIX': "/admin",
    'SECURITY_PASSWORD_HASH': "pbkdf2_sha512",
    'SECURITY_PASSWORD_SALT': "test",
    'SECURITY_LOGIN_URL': "/login/",
    'SECURITY_LOGOUT_URL': "/logout/",
    'SECURITY_REGISTER_URL': "/register/",
    'SECURITY_POST_LOGIN_VIEW': "/",
    'SECURITY_POST_LOGOUT_VIEW': "/",
    'SECURITY_POST_REGISTER_VIEW': "/",
}


@fixture
def app(request):
    test_config = dict(TEST_CONFIG)
    app = create_app(test_config)
    login_manager = LoginManager()
    login_manager.init_app(app)
    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    # mail = Mail(app)
    app_context = app.app_context()
    app_context.push()
    db.create_all()

    @app.route('/post_login')
    @login_required
    def post_login():
        return render_template('index.html', content='Post Login')

    @request.addfinalizer
    def fin():
        app_context.pop()

    return app


@fixture
def client(app):
    client = TestApp(app)
    return client
