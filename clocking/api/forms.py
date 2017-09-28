import re

from wtforms import DateField

from wtforms import Form, TextAreaField, validators
from wtforms.validators import ValidationError

from clocking.models import PersonMac, db


def validate_mac_address(form, field):
    """Validate the MAC address using a regex."""
    if field.data is not u'':
        if not re.match("[0-9A-Fa-f]{2}([ :])[0-9A-Fa-f]{2}(\\1[0-9A-Fa-f]{2}){4}$", field.data):
            raise ValidationError('MAC Address invalid.')


def validate_mac_address_unique_add(form, field):
    if field.data is not u'':
        if PersonMac.query.filter(PersonMac.mac == field.data).count() > 0:
            raise ValidationError('MAC Address already exists.')


def validate_mac_address_unique_edit(form, field):
    if field.data is not u'':
        person_mac = PersonMac.query.filter(PersonMac.mac == field.data)
        if person_mac.count() > 1:
            raise ValidationError('MAC Address already exists.')
        elif person_mac.count() == 1:
            person_mac = person_mac.first()
            if form.last_name.data != person_mac.last_name and \
                            form.first_name.data != person_mac.first_name:
                raise ValidationError('MAC Address already exists.')


class MacAddressField(TextAreaField):

    def process_formdata(self, valuelist):
        super(MacAddressField, self).process_formdata(valuelist)
        self.data = self.data.replace(':', ' ').upper()


class AddForm(Form):
    last_name = TextAreaField('Last name**', validators=[validators.required()])
    first_name = TextAreaField('First name*', validators=[validators.required()])
    mac1 = MacAddressField('MAC Address 1*',
                           validators=[validators.required(),
                                       validate_mac_address,
                                       validate_mac_address_unique_add])
    mac2 = MacAddressField('MAC Address 2',
                           validators=[validate_mac_address,
                                       validate_mac_address_unique_add])
    mac3 = MacAddressField('MAC Address 3',
                           validators=[validate_mac_address,
                                       validate_mac_address_unique_add])

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
    last_name = TextAreaField('Last name*', validators=[validators.required()])
    first_name = TextAreaField('First name*', validators=[validators.required()])
    mac = MacAddressField('MAC Address 1*',
                          validators=[validators.required(),
                                      validate_mac_address,
                                      validate_mac_address_unique_edit])

    def save(self, person_id):
        try:
            db.session.query(PersonMac).filter_by(id=person_id).update(
                self.data)
            db.session.commit()
        except:
            db.session.rollback()


def validate_start_date(form, field):
    if field.data >= form.end_date.data:
        raise ValidationError('Start date must be lower than end date.')


class SelectForm(Form):
    start_date = DateField('Start date', format="%d/%m/%Y",
                           validators=[validate_start_date])
    end_date = DateField('End date', format="%d/%m/%Y")
