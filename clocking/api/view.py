import json
import os

from datetime import timedelta, date, datetime
from flask import render_template, request, redirect, Response, send_from_directory, session, flash
from flask.views import MethodView

from clocking.models import db, Person, Entry, Address
from clocking.api.forms import PersonForm, MacForm, SelectForm, LoginForm
from clocking.api.generate_report import generate_report

from instance.settings import REPORT_DIR, REPORT_FILE


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


class MacDeleteView(MethodView):

    def get(self, mac_address):
        address = db.session.query(Address).get(mac_address)
        return render_template('delete.html', address=address)

    def post(self, mac_address):
        address = db.session.query(Address).get(mac_address)
        address.deleted = True
        try:
            db.session.commit()
        except:
            db.session.rollback()

        persons = filter_persons_addresses()
        return render_template('people.html', persons=persons)


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
        persons = filter_persons_addresses()
        return render_template('people.html', persons=persons)


class PersonClockingView(MethodView):

    def get(self):
        form = SelectForm()
        start_date, end_date = date.today(), date.today()
        if request.args:
            form = SelectForm(request.args)
            if form.validate():
                start_date = form.data.get('start_date')
                end_date = form.data.get('end_date')
        days = get_days(start_date, end_date)
        entries = get_all_entries(days)
        return render_template('clocking.html', form=form, entries=entries,
                               start_date=start_date, end_date=end_date)


class DownloadView(MethodView):

    def get(self, start_date, end_date):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        days = get_days(start_date, end_date)
        entries = get_all_entries(days)
        generate_report(entries)
        file = send_from_directory(directory=REPORT_DIR,
                                   filename=REPORT_FILE,
                                   as_attachment=True)
        os.remove(REPORT_DIR + REPORT_FILE)
        return file


class LoginView(MethodView):
    url = '/'

    def get(self):
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return "You are already logged in!"

    def post(self):
        form = LoginForm(request.form)
        if form.username.data == 'admin' and form.password.data == 'admin':
            session['logged_in'] = True

        return redirect(self.url, code=302)


class LogoutView(MethodView):
    url = '/'

    def get(self):
        if session.get('logged_in'):
            session['logged_in'] = False
            return redirect(self.url, code=302)
        else:
            return "You are already logged out!"


class AboutView(MethodView):

    def get(self):
        return render_template('about.html')



def filter_persons_addresses():
    persons = Person.query.join(Address).filter(
        Address.deleted==False).order_by(Person.first_name)
    for person in persons:
        person.addresses = [address for address in person.addresses if
                            address.deleted is False]
    return persons


def get_days(start_date, end_date):
    interval = end_date - start_date
    days = []
    for i in range(interval.days + 1):
        days.append(start_date + timedelta(days=i))
    return days


def get_all_entries(days):
    entries = []
    for day in days:
        entry = {}
        entry['day'] = day
        entry['entries_by_day'] = get_entries_by_day(day).all()
        if entry['entries_by_day']:
            entries.append(entry)
    return entries


def get_entries_by_day(day):
    entries = Entry.query
    return entries.filter(Entry.startdate >= day).filter(
        Entry.startdate <= day + timedelta(hours=24)).order_by(
        Entry.startdate)
