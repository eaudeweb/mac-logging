import re

from wtforms import Form, TextAreaField, validators, SelectField, fields
from flask import flash

from clocking.definitions import PERIODS
from clocking.models import PersonMac, db


class BaseForm(Form):
    def is_mac_address_valid(self, macs):
        """Validate the MAC addresses using a regex."""
        for mac in macs:
            if not re.match("[0-9A-Fa-f]{2}([ :])[0-9A-Fa-f]{2}(\\1[0-9A-Fa-f]{2}){4}$", mac):
                return False
        return True

    def convert_mac_format(self, mac):
        return mac.replace(':', ' ').upper()


class AddForm(BaseForm):
    last_name = TextAreaField('Nume*', validators=[validators.required()])
    first_name = TextAreaField('Prenume*', validators=[validators.required()])
    mac1 = TextAreaField('Adresa MAC 1*', validators=[validators.required()])
    mac2 = TextAreaField('Adresa MAC 2')
    mac3 = TextAreaField('Adresa MAC 3')

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

        if self.validate():
            if self.is_mac_address_valid(macs):
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


class EditForm(BaseForm):
    last_name = TextAreaField('Nume*', validators=[validators.required()])
    first_name = TextAreaField('Prenume*', validators=[validators.required()])
    mac = TextAreaField('Adresa MAC 1*', validators=[validators.required()])

    def save(self, person_id):
        data = self.data
        last_name = data['last_name']
        first_name = data['first_name']
        macs = []
        mac = data['mac']
        mac = self.convert_mac_format(mac)
        macs.append(mac)

        if self.validate():
            if self.is_mac_address_valid(macs):
                data = {
                    "last_name": last_name,
                    "first_name": first_name,
                    "mac": mac
                }
                try:
                    flash(data)
                    db.session.query(PersonMac).filter_by(id=person_id).update(
                        data)
                    db.session.commit()
                    flash('Thanks for editing.')
                except:
                    db.session.rollback()
                    flash('Error: Editing failed. '
                          'Possibly MAC address already exists.')
            else:
                flash('Error: MAC Address invalid.')
        else:
            flash('Error: All the form fields with * are required. ')


class SelectForm(Form):
    periods = SelectField(
        'Pontaj',
        choices=PERIODS
    )
