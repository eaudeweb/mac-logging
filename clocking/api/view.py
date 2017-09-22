from datetime import timedelta, datetime

from flask import render_template, request, flash
from flask.views import MethodView

from clocking.models import PersonMac, Person, MacAddress, db
from clocking.api.forms import AddForm, EditForm, SelectForm


class BaseView(MethodView):
    def convert_mac_format(self, mac):
        return mac.replace(':', ' ').upper()


class PersonAddView(BaseView):

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
                    mac = self.convert_mac_format(mac)
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


class PersonEditView(BaseView):

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
        mac = self.convert_mac_format(mac)
        macs.append(mac)

        if form.validate():
            if form.is_mac_address_valid(macs):
                data = {
                    "last_name": last_name,
                    "first_name": first_name,
                    "mac": mac
                    }
                try:
                    flash(data)
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

        if days == 'Astazi':
            return Person.query.filter(
                Person.startdate.between(date1, date2)).order_by(Person.startdate)
        elif days == 'Saptamana curenta':
            while date1.weekday() != 0:
                date1 -= timedelta(days=1)
            return Person.query.filter(
                Person.startdate.between(date1, date2)).order_by(Person.startdate)
        elif days == 'Luna curenta':
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