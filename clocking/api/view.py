from datetime import timedelta
from sqlalchemy import extract
import json
from flask import render_template, request, Response
from flask.views import MethodView

from clocking.models import Person
from clocking.api.forms import PersonForm, MacForm


class PersonAddView(MethodView):

    def get(self):
        form = PersonForm()
        return render_template('add.html', form=form)

    def post(self):
        data = {}
        form = PersonForm(request.form)
        if form.validate():
            person = form.save()
            data['html'] = render_template('bits/mac_form.html', person=person)
            data['status'] = 'success'
        else:
            data['html'] = render_template('bits/form_errors.html', form=form)
            data['status'] = 'error'

        return Response(json.dumps(data), content_type='application/json')


class MacAddView(MethodView):

    def post(self):
        data = {}
        form = MacForm(request.form)
        if form.validate():
            address = form.save()
            data['html'] = render_template('bits/mac_listing.html',
                                           address=address)
            data['status'] = 'success'
        else:
            data['html'] = render_template('bits/form_errors.html',
                                           form=form)
            data['status'] = 'error'

        return Response(json.dumps(data), content_type='application/json')

# class PersonEditView(MethodView):
#
#     def get(self, person_id):
#         person = db.session.query(PersonMac).get(person_id)
#         form = EditForm()
#         return render_template('edit.html', form=form, person=person)
#
#     def post(self, person_id):
#         person = db.session.query(PersonMac).get(person_id)
#         form = EditForm(request.form)
#         if form.validate():
#             form.save(person_id)
#             persons = PersonMac.query.order_by(PersonMac.last_name)
#             return render_template('people.html', persons=persons,
#                                    success="You've successfully edited a person")
#
#         return render_template('edit.html', form=form, person=person)
#
#
# class PersonListView(MethodView):
#
#     def get(self):
#         persons = PersonMac.query.order_by(PersonMac.last_name)
#         return render_template('people.html', persons=persons)
#
#
# class PersonClockingView(MethodView):
#     def get_persons_by_interval(self, start_date, end_date):
#         persons = Person.query
#         if start_date and end_date:
#             return persons.filter(Person.startdate.between(start_date, end_date)).order_by(Person.startdate)
#         else:
#             return persons.all()
#
#     def get(self):
#         form = SelectForm()
#
#         start_date, end_date = None, None
#         if request.args:
#             form = SelectForm(request.args)
#             if form.validate():
#                 start_date = form.data.get('start_date')
#                 end_date = form.data.get('end_date')
#
#         persons = self.get_persons_by_interval(start_date, end_date)
#
#         return render_template('clocking.html', form=form, persons=persons)
