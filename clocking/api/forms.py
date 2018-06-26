import re

from datetime import datetime
from wtforms import DateField, Form, TextAreaField, IntegerField, DateTimeField, validators
from wtforms.validators import ValidationError
from flask_security import current_user

from clocking.models import Person, Address, Entry, Departament, db


def validate_mac_address(form, field):
    """Validate the MAC address using a regex."""
    if field.data is not u'':
        if not re.match("[0-9A-Fa-f]{2}([ :])[0-9A-Fa-f]{2}(\\1[0-9A-Fa-f]{2}){4}$", field.data):
            raise ValidationError('MAC Address invalid.')


class PersonForm(Form):
    last_name = TextAreaField('Last name',
                              validators=[validators.required()])
    first_name = TextAreaField('First name',
                               validators=[validators.required()])
    dept = IntegerField('dept',
                        validators=[validators.required()])

    def save(self, person_id=None):
        if person_id:
            person = db.session.query(Person).filter_by(id=person_id)
            dept = Departament.query.get(self.data['dept'])
            person.update({
                'id': person_id,
                'first_name': self.data['first_name'],
                'last_name': self.data['last_name'],
                'dept_id': dept.id
            })
            person = person.first()
        else:
            dept = Departament.query.get(self.data['dept'])
            person = Person(first_name=self.data['first_name'], last_name=self.data['last_name'],
                            dept=dept)
            db.session.add(person)

        try:
            db.session.commit()
            if not person_id:   # if it is a create, we link the person to the current user
                current_user.person_id = person.id
                db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

        return person


def validate_mac_address_unique_add(form, field):
    if field.data is not u'':
        if Address.query.filter(Address.mac == field.data).count() > 0:
            raise ValidationError('MAC Address already exists.')


class MacAddressField(TextAreaField):

    def process_formdata(self, valuelist):
        super(MacAddressField, self).process_formdata(valuelist)
        self.data = self.data.replace(':', ' ').upper()


class MacForm(Form):
    mac = MacAddressField('MAC Address',
                          validators=[validators.required(),
                                      validate_mac_address,
                                      validate_mac_address_unique_add])
    device = TextAreaField('Device', validators=[validators.required()])
    person = IntegerField('Person', validators=[validators.required()])
    priority = TextAreaField('Priority', validators=[validators.required()])

    def save(self):
        person = self.data.pop('person')
        person = Person.query.get(person)
        address = Address(person=person, mac=self.data['mac'],
                          device=self.data['device'], priority=self.data['priority'])
        db.session.add(address)
        try:
            db.session.commit()
        except:
            db.session.rollback()

        return address


class SelectForm(Form):
    start_date = DateField('Start date', format="%d/%m/%Y",
                           validators=[validators.required()])
    end_date = DateField('End date', format="%d/%m/%Y",
                         validators=[validators.required()])


class ManualEntryForm(Form):
    mac = MacAddressField('MAC Address',
                          validators=[validators.required(),
                                      validate_mac_address])
    time_in = DateTimeField('Time in', format='%H:%M')
    time_out = DateTimeField('Time out', format='%H:%M')

    def save(self):
        now = datetime.now()
        startdate = now.replace(hour=self.data['time_in'].hour,
                                minute=self.data['time_in'].minute,
                                second=self.data['time_in'].second)
        enddate = now.replace(hour=self.data['time_out'].hour,
                              minute=self.data['time_out'].minute,
                              second=self.data['time_out'].second)
        entry = Entry(mac_id=self.data['mac'],
                      startdate=startdate,
                      enddate=enddate)
        db.session.add(entry)
        try:
            db.session.commit()
        except:
            db.session.rollback()

        return entry
