"""add_priority

Revision ID: fcb160a4037f
Revises: 0ebf504d1381
Create Date: 2018-06-22 01:05:17.782451

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import (
    Column, String, ForeignKey, Integer, DateTime, Boolean
)
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import ChoiceType
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin


# revision identifiers, used by Alembic.
revision = 'fcb160a4037f'
down_revision = '0ebf504d1381'
branch_labels = None
depends_on = None

db = SQLAlchemy()
Session = sessionmaker()


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
    PRIORITIES = [
        (u'2', u'low'),
        (u'1', u'medium'),
        (u'0', u'high')
    ]

    mac = Column(String(128), primary_key=True)
    device = Column(ChoiceType(DEVICES), nullable=False)
    person_id = Column(ForeignKey('person.id'))
    deleted = Column(Boolean, default=False)
    exittime = Column(DateTime, nullable=True)
    priority = Column(ChoiceType(PRIORITIES), nullable=False, default='2')

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


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('address', sa.Column('priority', ChoiceType(Address.PRIORITIES), nullable=False,
                                       server_default='2'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('address', 'priority')
    # ### end Alembic commands ###
