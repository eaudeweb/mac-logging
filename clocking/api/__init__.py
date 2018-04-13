from flask import Blueprint
from flask_script import Manager

from clocking.api.view import (MacAddView, PersonAddView, PersonEditView,
                               PersonListView, PersonClockingView, AboutView,
                               MacDeleteView, DownloadView)

api = Blueprint('api', __name__)
api_manager = Manager()

api.add_url_rule('/add', view_func=PersonAddView.as_view('add'))
api.add_url_rule('/add_mac', view_func=MacAddView.as_view('add_mac'))
api.add_url_rule('/delete_mac/<mac_address>', view_func=MacDeleteView.as_view('delete_mac'))
api.add_url_rule('/edit/<person_id>', view_func=PersonEditView.as_view('edit'))
api.add_url_rule('/people', view_func=PersonListView.as_view('people'))
api.add_url_rule('/', view_func=PersonClockingView.as_view('clocking'))
api.add_url_rule('/download/<start_date>/<end_date>', view_func=DownloadView.as_view('download'))
api.add_url_rule('/about', view_func=AboutView.as_view('about'))
