import json
from datetime import timedelta
from flask import render_template, request, Response
from flask.views import MethodView

from clocking.models import db, Person, Entry
from clocking.api.forms import PersonForm, MacForm, SelectForm


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


class PersonEditView(MethodView):
    def get(self, person_id):
        person = db.session.query(Person).get(person_id)
        person_form = PersonForm()
        mac_form = MacForm()
        return render_template('edit.html', person_form=person_form,
                               mac_form=mac_form, person=person)

    def post(self, person_id):
        data = {}
        form = PersonForm(request.form)
        if form.validate():
            person = form.save(person_id)
            data['html'] = render_template('bits/person_edit.html',
                                           person=person)
            data['status'] = 'success'
        else:
            data['html'] = render_template('bits/person_edit.html',
                                           form=form)
            data['status'] = 'error'

        return Response(json.dumps(data), content_type='application/json')


class PersonListView(MethodView):

    def get(self):
        persons = Person.query.order_by(Person.first_name)
        return render_template('people.html', persons=persons)


class PersonClockingView(MethodView):
    def get_entries_by_interval(self, start_date, end_date):
        entries = Entry.query
        if start_date and end_date:
            return entries.filter(Entry.startdate >= start_date).filter(
                Entry.startdate <= end_date + timedelta(hours=24)).order_by(
                Entry.startdate)
        else:
            return entries.all()

    def get(self):
        form = SelectForm()

        start_date, end_date = None, None
        if request.args:
            form = SelectForm(request.args)
            if form.validate():
                start_date = form.data.get('start_date')
                end_date = form.data.get('end_date')

        entries = self.get_entries_by_interval(start_date, end_date)

        return render_template('clocking.html', form=form, entries=entries)


class AboutView(MethodView):

    def get(self):
        return render_template('about.html')
