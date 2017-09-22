import re

from wtforms import Form, TextAreaField, validators, SelectField


class BaseForm(Form):
    def is_mac_address_valid(self, macs):
        """Validate the MAC addresses using a regex."""
        for mac in macs:
            if not re.match("[0-9A-Fa-f]{2}([ :])[0-9A-Fa-f]{2}(\\1[0-9A-Fa-f]{2}){4}$",
                            mac):
                return False
        return True


class AddForm(BaseForm):
    last_name = TextAreaField('Nume*', validators=[validators.required()])
    first_name = TextAreaField('Prenume*', validators=[validators.required()])
    mac1 = TextAreaField('Adresa MAC 1*', validators=[validators.required()])
    mac2 = TextAreaField('Adresa MAC 2')
    mac3 = TextAreaField('Adresa MAC 3')


class EditForm(BaseForm):
    last_name = TextAreaField('Nume*', validators=[validators.required()])
    first_name = TextAreaField('Prenume*', validators=[validators.required()])
    mac = TextAreaField('Adresa MAC 1*', validators=[validators.required()])


class SelectForm(Form):
    days = SelectField(
        'Pontaj',
        choices=['Astazi', 'Saptamana curenta', 'Luna curenta']
    )