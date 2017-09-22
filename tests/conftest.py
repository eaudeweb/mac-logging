from flask.ext.webtest import TestApp
from pytest import fixture

from clocking.models import db
from clocking.app import create_app

TEST_CONFIG = {
    'DEBUG': True,
    'SERVER_NAME': 'noname',
    'SECRET_KEY': 'secret',
}

@fixture
def app(request):
    test_config = dict(TEST_CONFIG)
    app = create_app(test_config)
    app_context = app.app_context()
    app_context.push()
    db.create_all()

    @request.addfinalizer
    def fin():
        app_context.pop()

    return app


@fixture
def client(app):
    client = TestApp(app)
    return client
