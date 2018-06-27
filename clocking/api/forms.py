import re

from datetime import datetime
from wtforms import DateField, Form, TextAreaField, IntegerField, DateTimeField, PasswordField, validators
from wtforms.validators import ValidationError
from flask_security import SQLAlchemyUserDatastore, current_user, utils

from clocking.models import Person, Address, Entry, Departament, User, Role, db


EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def validate_mac_address_unique_add(form, field):
    if field.data is not u'':
        if Address.query.filter(Address.mac == field.data).count() > 0:
            raise ValidationError('MAC Address already exists.')


def validate_mac_address(form, field):
    """Validate the MAC address using a regex."""
    if field.data is not u'':
        if not re.match("[0-9A-Fa-f]{2}([ :])[0-9A-Fa-f]{2}(\\1[0-9A-Fa-f]{2}){4}$", field.data):
            raise ValidationError('MAC Address invalid.')


def validate_email_unique(form, field):
    if field.data is not u'':
        if User.query.filter(User.email == field.data).count () > 0:
            raise ValidationError('Email already exists.')


def validate_email_format(form, field):
    if field.data is not u'':
        if not EMAIL_REGEX.match(field.data):
            raise ValidationError('Invalid E-Mail addresss format.')


#TODO check if confirm_password is the same as password


class BasePersonForm(Form):
    last_name = TextAreaField('Last name',
                              validators=[validators.required()])
    first_name = TextAreaField('First name',
                               validators=[validators.required()])
    dept = IntegerField('dept',
                        validators=[validators.required()])


class PersonForm(BasePersonForm, Form):

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
            if person_id:
                db.session.commit()
            else:   # else, if it is a create, we link the person to the current user
                current_user.person_id = person.id
                db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        return person


class AdminUserForm(Form):
    email = TextAreaField('Email',
                          validators=[validators.required(),
                                      validate_email_unique,
                                      validate_email_format])
    password = PasswordField('Password',
                             validators=[validators.required()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[validators.required()])

    def save(self):
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        user = user_datastore.create_user(
            email=self.data['email'],
            password=utils.encrypt_password(self.data['password'])
        )
        db.session.commit()
        user_datastore.add_role_to_user(self.data['email'], 'user')
        db.session.commit()
        return user


class AdminPersonForm(BasePersonForm, Form):
    user_id = IntegerField('User', validators=[validators.required()])

    def save(self):
        dept = Departament.query.get(self.data['dept'])
        person = Person(first_name=self.data['first_name'], last_name=self.data['last_name'],
                        dept=dept)
        db.session.add(person)
        user = User.query.get(self.data['user_id'])
        user.person_id = person.id
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        return person


class AdminPersonEditForm(BasePersonForm, Form):

    def save(self, person_id):
        person = db.session.query(Person).filter_by(id=person_id)
        dept = Departament.query.get(self.data['dept'])
        person.update({
            'id': person_id,
            'first_name': self.data['first_name'],
            'last_name': self.data['last_name'],
            'dept_id': dept.id
        })
        person = person.first()
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        return person


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
