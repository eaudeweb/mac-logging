import re

from datetime import timedelta
from wtforms import DateField

from wtforms import Form, TextAreaField, IntegerField, validators
from wtforms.validators import ValidationError

from clocking.models import Person, Address, db


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

    def save(self, person_id=None):
        if person_id:
            person = db.session.query(Person).filter_by(id=person_id)
            person.update(self.data)
            person = person.first()
        else:
            person = Person(**self.data)
            db.session.add(person)
        try:
            db.session.commit()
        except:
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

    def save(self):
        person = self.data.pop('person')
        person = Person.query.get(person)
        address = Address(person=person, mac=self.data['mac'],
                          device=self.data['device'])
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


class LoginForm(Form):
    username = TextAreaField()
    password = TextAreaField()
