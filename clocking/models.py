from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from flask_security import UserMixin, RoleMixin, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager

db = SQLAlchemy()
db_manager = Manager()


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    ROLES = [
        (u'superuser', u'Superuser'),
        (u'user', u'User')
    ]
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(ChoiceType(ROLES), unique=True)
    users = Column(ForeignKey('user.id'))

    def __str__(self):
        return self.name.value


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    person_id = Column(Integer, ForeignKey('person.id'))

    roles = relationship('Role', backref=db.backref('users_role'))

    def __str__(self):
        return self.email


class Address(db.Model):
    __tablename__ = 'address'
    DEVICES = [
        (u'mobile', u'Mobile'),
        (u'laptop', u'Laptop'),
        (u'desktop', u'Desktop')
    ]

    mac = Column(String(128), primary_key=True)
    device = Column(ChoiceType(DEVICES), nullable=False)
    person_id = Column(ForeignKey('person.id'))
    deleted = Column(Boolean, default=False)
    exittime = Column(DateTime, nullable=True)

    person = relationship('Person',
                          backref=db.backref('addresses', lazy='dynamic'))

    def __str__(self):
        return self.mac


class Person(db.Model):
    """ Person model """
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    dept_id = Column(ForeignKey('departament.id'))

    user = relationship("User", uselist=False, backref="person")
    dept = relationship('Departament',
                        backref=db.backref('persons', lazy='dynamic'))

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Entry(db.Model):
    __tablename__ = 'entry'
    id = Column(Integer, primary_key=True, autoincrement=True)
    mac_id = Column(ForeignKey('address.mac'))
    startdate = Column(DateTime, nullable=False)
    enddate = Column(DateTime)
    comment = Column(db.Text)

    mac = relationship('Address',
                       backref=db.backref('entries', lazy='dynamic'))


class Departament(db.Model):
    __tablename__ = 'departament'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(db.String(255), unique=True)

    def __str__(self):
        return self.name
