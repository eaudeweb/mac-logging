import re

from wtforms import DateField, SelectField

from wtforms import Form, TextAreaField, validators
from wtforms.validators import ValidationError

from clocking.definitions import PERIODS

from clocking.models import PersonMac, db


def validate_mac_address(form, field):
    """Validate the MAC address using a regex."""
    if field.data is not u'':
        if not re.match("[0-9A-Fa-f]{2}([ :])[0-9A-Fa-f]{2}(\\1[0-9A-Fa-f]{2}){4}$", field.data):
            raise ValidationError('MAC Address invalid.')


class MacAddressField(TextAreaField):

    def process_formdata(self, valuelist):
        super(MacAddressField, self).process_formdata(valuelist)
        self.data = self.data.replace(':', ' ').upper()


class AddForm(Form):
    last_name = TextAreaField('Nume*', validators=[validators.required()])
    first_name = TextAreaField('Prenume*', validators=[validators.required()])
    mac1 = MacAddressField('Adresa MAC 1*', validators=[validators.required(),
                                                        validate_mac_address])
    mac2 = MacAddressField('Adresa MAC 2', validators=[validate_mac_address])
    mac3 = MacAddressField('Adresa MAC 3', validators=[validate_mac_address])

    def save(self):
        data = self.data
        last_name = data['last_name']
        first_name = data['first_name']
        macs = []
        mac1 = data['mac1']
        macs.append(mac1)
        mac2 = data['mac2']
        if mac2 is not u'':
            macs.append(mac2)
        mac3 = data['mac3']
        if mac3 is not u'':
            macs.append(mac3)

        for mac in macs:
            person_mac = PersonMac(last_name, first_name, mac)
            db.session.add(person_mac)
        try:
            db.session.commit()
        except:
            db.session.rollback()


class EditForm(Form):
    last_name = TextAreaField('Nume*', validators=[validators.required()])
    first_name = TextAreaField('Prenume*', validators=[validators.required()])
    mac = MacAddressField('Adresa MAC 1*', validators=[validators.required()])

    def save(self, person_id):
        try:
            db.session.query(PersonMac).filter_by(id=person_id).update(
                self.data)
            db.session.commit()
        except:
            db.session.rollback()


class SelectForm(Form):
    periods = SelectField(
        'Pontaj',
        choices=PERIODS
    )
