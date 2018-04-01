from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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

    person = relationship('Person',
                          backref=db.backref('addresses', lazy='dynamic'))

    def __unicode__(self):
        return self.mac


class Person(db.Model):
    """ Person model """
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name


class Entry(db.Model):
    __tablename__ = 'entry'
    id = Column(Integer, primary_key=True, autoincrement=True)
    mac_id = Column(ForeignKey('address.mac'))
    startdate = Column(DateTime, nullable=False)

    mac = relationship('Address',
                       backref=db.backref('entries', lazy='dynamic'))
