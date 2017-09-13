# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash, request
from flask.views import MethodView
from wtforms import Form, TextAreaField, SelectField, validators
from models import db, PersonMac, MacAddress, Person
from datetime import datetime, timedelta
import re

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# App config.
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('settings.py', silent=True)

if app.config.get('SENTRY_DSN'):
    from raven.contrib.flask import Sentry
    Sentry(app)

db.init_app(app)
migrate = Migrate(app, db)


class BaseForm(Form):
    def is_mac_address_valid(self, macs):
        """Validate the MAC addresses using a regex."""
        for mac in macs:
            if not re.match("[0-9A-F]{2}([ ])[0-9A-F]{2}(\\1[0-9A-F]{2}){4}$",
                            mac):
                return False
        return True


class AddForm(BaseForm):
    last_name = TextAreaField('Nume*', validators=[validators.required()])
    first_name = TextAreaField('Prenume*', validators=[validators.required()])
    mac1 = TextAreaField('Adresă MAC 1*', validators=[validators.required()])
    mac2 = TextAreaField('Adresă MAC 2')
    mac3 = TextAreaField('Adresă MAC 3')


class EditForm(BaseForm):
    last_name = TextAreaField('Nume*', validators=[validators.required()])
    first_name = TextAreaField('Prenume*', validators=[validators.required()])
    mac = TextAreaField('Adresă MAC 1*', validators=[validators.required()])


class SelectForm(Form):
    days = SelectField(
        'Pontaj',
        choices=['Astăzi', 'Săptămâna curentă', 'Luna curentă']
    )


class PersonAddView(MethodView):

    def get(self):
        form = AddForm()
        return render_template('add.html', form=form)

    def post(self):
        form = AddForm(request.form)
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        macs = []
        mac1 = request.form['mac1']
        macs.append(mac1)
        mac2 = request.form['mac2']
        if mac2 is not u'':
            macs.append(mac2)
        mac3 = request.form['mac3']
        if mac3 is not u'':
            macs.append(mac3)

        if form.validate():
            if form.is_mac_address_valid(macs):
                for mac in macs:
                    person_mac = PersonMac(last_name, first_name, mac)
                    db.session.add(person_mac)

                try:
                    db.session.commit()
                    flash('Thanks for registration.')
                except:
                    db.session.rollback()
                    flash('Error: Registration failed. '
                          'Possibly MAC address already exists.')
            else:
                flash('Error: MAC Address invalid.')
        else:
            flash('Error: All the form fields with * are required. ')

        return render_template('add.html', form=form)


class PersonEditView(MethodView):

    def get(self, person_id):
        person = db.session.query(PersonMac).get(person_id)
        form = EditForm()
        return render_template('edit.html', form=form, person=person)

    def post(self, person_id):
        person = db.session.query(PersonMac).get(person_id)
        form = EditForm(request.form)
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        macs = []
        mac = request.form['mac']
        macs.append(mac)

        if form.validate():
            if form.is_mac_address_valid(macs):
                data = {
                    "last_name": last_name,
                    "first_name": first_name,
                    "mac": mac
                    }
                try:
                    db.session.query(PersonMac).filter_by(id=person_id).update(data)
                    flash('Thanks for editing.')
                except:
                    db.session.rollback()
                    flash('Error: Editing failed. '
                          'Possibly MAC address already exists.')
            else:
                flash('Error: MAC Address invalid.')
        else:
            flash('Error: All the form fields with * are required. ')

        return render_template('edit.html', form=form, person=person)


class PersonListView(MethodView):

    def get(self):
        persons = PersonMac.query.order_by(PersonMac.last_name)

        return render_template('people.html', persons=persons)


class PersonClockingView(MethodView):

    def map_persons(self):
        mac_addresses = MacAddress.query.all()

        for mac_address in mac_addresses:
            persons_mac = PersonMac.query.filter(PersonMac.mac == mac_address.mac).all()
            for person_mac in persons_mac:
                startdate = mac_address.time
                enddate = startdate
                enddate += timedelta(hours=8)
                db.session.add(Person(person_mac.last_name, person_mac.first_name,
                                      startdate, enddate))
                try:
                    db.session.commit()
                except:
                    db.session.rollback()

    def get_persons(self, days):
        date1 = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
        date2 = date1 + timedelta(hours=23, minutes=59, seconds=59)

        if days == 'Astăzi':
            return Person.query.filter(
                Person.startdate.between(date1, date2)).order_by(Person.startdate)
        elif days == 'Săptămâna curentă':
            while date1.weekday() != 0:
                date1 -= timedelta(days=1)
            return Person.query.filter(
                Person.startdate.between(date1, date2)).order_by(Person.startdate)
        elif days == 'Luna curentă':
            while date1.day != 1:
                date1 -= timedelta(days=1)
            return Person.query.filter(
                Person.startdate.between(date1, date2)).order_by(Person.startdate)

        return Person.query.order_by(Person.startdate)

    def get(self):
        self.map_persons()
        persons = Person.query.order_by(Person.startdate)

        return render_template('clocking.html', persons=persons)

    def post(self):
        form = SelectForm(request.form)
        days = request.form['sel1']
        persons = self.get_persons(days)

        return render_template('clocking.html', persons=persons)


class IndexView(MethodView):

    def get(self):
        return render_template('index.html')


@app.context_processor
def utility_processor():
    def get_enddate(enddate):
        if enddate < datetime.now():
            return enddate
        else:
            return '-'
    return dict(get_enddate=get_enddate)


@app.route('/crashme')
def crashme():
    raise RuntimeError("Crashing as requested by you")

app.add_url_rule('/add', view_func=PersonAddView.as_view('add'))
app.add_url_rule('/edit/<person_id>', view_func=PersonEditView.as_view('edit'))
app.add_url_rule('/people', view_func=PersonListView.as_view('people'))
app.add_url_rule('/clocking', view_func=PersonClockingView.as_view('clocking'))
app.add_url_rule('/', view_func=IndexView.as_view('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, host='0.0.0.0', port=5000)
