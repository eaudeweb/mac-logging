import json
import os

from datetime import timedelta, date, datetime
from flask import render_template, request, redirect, Response, send_from_directory, session, url_for, abort
from flask.views import MethodView
from flask_admin.contrib import sqla
from flask_restful import Resource
from flask_security import current_user
from sqlalchemy import and_

from clocking.models import db, Person, Entry, Address
from clocking.api.forms import PersonForm, MacForm, SelectForm, LoginForm
from clocking.api.generate_report import generate_report

from instance.settings import REPORT_DIR, REPORT_FILE


class ProtectedModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))


class PersonAddView(MethodView):

    def get(self):
        if current_user.is_authenticated:
            form = PersonForm()
            return render_template('add.html', form=form)
        else:
            abort(403)

    def post(self):
        if current_user.is_authenticated:
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
        else:
            abort(403)


class MacAddView(MethodView):

    def post(self):
        if current_user.is_authenticated:
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
        else:
            abort(403)


class MacDeleteView(MethodView):

    def get(self, mac_address):
        if current_user.is_authenticated and current_user.has_role('superuser'):
            address = db.session.query(Address).get(mac_address)
            return render_template('delete.html', address=address)
        else:
            abort(403)

    def post(self, mac_address):
        if current_user.is_authenticated and current_user.has_role('superuser'):
            address = db.session.query(Address).get(mac_address)
            address.deleted = True
            try:
                db.session.commit()
            except:
                db.session.rollback()
            persons = filter_persons_addresses()
            return render_template('people.html', persons=persons)
        else:
            abort(403)


class PersonEditView(MethodView):

    def get(self, person_id):
        if current_user.is_authenticated and (
                current_user.has_role('superuser') or current_user.person_id == int(person_id)):
            person = db.session.query(Person).get(person_id)
            person_form = PersonForm()
            mac_form = MacForm()
            return render_template('edit.html', person_form=person_form,
                                   mac_form=mac_form, person=person)
        else:
            abort(403)

    def post(self, person_id):
        if current_user.is_authenticated and current_user.has_role('superuser'):
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
        else:
            abort(403)


class PersonListView(MethodView):

    def get(self):
        if current_user.is_authenticated and current_user.has_role('superuser'):
            persons = filter_persons_addresses()
            return render_template('people.html', persons=persons)
        else:
            abort(403)


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
        if current_user.is_authenticated and current_user.has_role('superuser'):
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
        else:
            abort(403)


class AboutView(MethodView):

    def get(self):
        return render_template('about.html')


class EntryAddResource(Resource):

    def get(self):
        return {'task': "I'll provide you an implementation soon!!!"}

    def post(self):
        data = request.get_json()
        addresses = data['addresses']
        print(addresses)
        last_modified = data["time"]
        last_modified = datetime.strptime(last_modified, "%a %b %d %H:%M:%S %Y")
        existing_addresses = [address.mac for address in
                              Address.query.filter(Address.deleted == False).all()]
        new_entries = []
        persons_ids = []
        for address in addresses:
            if address in existing_addresses:
                person_details = Person.query.join(Person.addresses).filter_by(
                    mac=address
                ).first()
                if person_details.id in persons_ids:
                    continue
                new_entries.append((
                    address,
                    person_details.last_name,
                    person_details.first_name
                ))
                persons_ids.append(person_details.id)

        startdate_datetime = last_modified.replace(minute=00, hour=00, second=00)

        for address, last_name, first_name in new_entries:
            find_any_values = Entry.query.filter(
                and_(Entry.startdate >= startdate_datetime.date(),
                     Entry.startdate <= startdate_datetime.date() + timedelta(days=1))
            ).join(Entry.mac).join(Address.person).filter_by(
                last_name=last_name,
                first_name=first_name
            )
            if find_any_values.count() == 0:
                entry = Entry(**{'mac_id': address,
                                 'startdate': last_modified})
                db.session.add(entry)
                db.session.commit()
        # TODO copy past the add logic


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
