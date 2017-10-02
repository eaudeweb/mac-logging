import re

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


def validate_mac_address_unique_edit(form, field):
    if field.data is not u'':
        person_mac = Address.query.filter(Address.mac == field.data)
        if person_mac.count() > 1:
            raise ValidationError('MAC Address already exists.')
        elif person_mac.count() == 1:
            person_mac = person_mac.first()
            if form.last_name.data != person_mac.last_name and \
                            form.first_name.data != person_mac.first_name:
                raise ValidationError('MAC Address already exists.')


# class EditForm(Form):
#     last_name = TextAreaField('Last name*', validators=[validators.required()])
#     first_name = TextAreaField('First name*', validators=[validators.required()])
#     mac = MacAddressField('MAC Address 1*',
#                           validators=[validators.required(),
#                                       validate_mac_address,
#                                       validate_mac_address_unique_edit])
#
#     def save(self, person_id):
#         try:
#             db.session.query(Address).filter_by(id=person_id).update(
#                 self.data)
#             db.session.commit()
#         except:
#             db.session.rollback()

#
#
# def validate_start_date(form, field):
#     if field.data >= form.end_date.data:
#         raise ValidationError('Start date must be lower than end date.')
#
#
# class SelectForm(Form):
#     start_date = DateField('Start date', format="%d/%m/%Y",
#                            validators=[validate_start_date])
#     end_date = DateField('End date', format="%d/%m/%Y")
