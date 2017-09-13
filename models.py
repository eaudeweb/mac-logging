from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from flask.flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MacAddress(db.Model):
    __tablename__ = 'mac_addresses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    mac = Column(String(128), unique=True)
    time = Column(DateTime, nullable=False)

    def __init__(self, mac=None, time=None):
        self.mac = mac
        self.time = time


class PersonMac(db.Model):
    """ Person model """
    __tablename__ = 'persons_mac'
    id = Column(Integer, primary_key=True, autoincrement=True)
    mac = Column(String(128), unique=True)
    last_name = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)

    def __init__(self, last_name=None, first_name=None, mac=None):
        self.last_name = last_name
        self.first_name = first_name
        self.mac = mac


class Person(db.Model):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    startdate = Column(DateTime, nullable=False)
    enddate = Column(DateTime, nullable=False)
    __table_args__ = (
        UniqueConstraint('last_name', 'first_name', 'enddate',
                         name='unique_columns'),
    )

    def __init__(self, last_name=None, first_name=None, startdate=None, enddate=None):
        self.last_name = last_name
        self.first_name = first_name
        self.startdate = startdate
        self.enddate = enddate
