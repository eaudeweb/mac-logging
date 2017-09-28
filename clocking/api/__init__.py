from flask import Blueprint
from flask.ext.script import Manager

from .view import PersonAddView, PersonEditView, PersonListView, \
    PersonClockingView

api = Blueprint('api', __name__)
api_manager = Manager()

api.add_url_rule('/add', view_func=PersonAddView.as_view('add'))
api.add_url_rule('/edit/<person_id>', view_func=PersonEditView.as_view('edit'))
api.add_url_rule('/people', view_func=PersonListView.as_view('people'))
api.add_url_rule('/', view_func=PersonClockingView.as_view('clocking'))
