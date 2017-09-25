from datetime import timedelta, datetime

from flask import render_template, request, flash
from flask.views import MethodView

from clocking.models import PersonMac, Person, MacAddress, db
from clocking.api.forms import AddForm, EditForm, SelectForm
from clocking.definitions import LAST_DAY, CURRENT_WEEK, CURRENT_MONTH, LAST_WEEK


class PersonAddView(MethodView):

    def get(self):
        form = AddForm()
        return render_template('add.html', form=form)

    def post(self):
        form = AddForm(request.form)
        form.save()
        return render_template('add.html', form=form)


class PersonEditView(MethodView):

    def get(self, person_id):
        person = db.session.query(PersonMac).get(person_id)
        form = EditForm()
        return render_template('edit.html', form=form, person=person)

    def post(self, person_id):
        person = db.session.query(PersonMac).get(person_id)
        form = EditForm(request.form)
        form.save(person_id)
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

    def get_persons(self, period):
        # default is TODAY
        start = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
        stop = start + timedelta(hours=23, minutes=59, seconds=59)

        if period == LAST_DAY:
            start -= timedelta(days=1)
            stop -= timedelta(days=1)
        elif period == CURRENT_WEEK:
            while start.weekday() != 0:
                start -= timedelta(days=1)
        elif period == LAST_WEEK:
            while start.weekday() != 0:
                start -= timedelta(days=1)
            start -= timedelta(days=7)
            stop -= timedelta(days=7)
            while stop.weekday() != 4:
                stop += timedelta(days=1)
        elif period == CURRENT_MONTH:
            while start.day != 1:
                start -= timedelta(days=1)

        return Person.query.filter(
            Person.startdate.between(start, stop)).order_by(Person.startdate)


    def get(self):
        self.map_persons()
        persons = Person.query.order_by(Person.startdate)

        return render_template('clocking.html', persons=persons)

    def post(self):
        form = SelectForm(request.form)
        period = request.form['sel1']
        persons = self.get_persons(period)

        return render_template('clocking.html', persons=persons)


class IndexView(MethodView):

    def get(self):
        return render_template('index.html')
