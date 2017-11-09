"""add_deleted_field

Revision ID: 5a8606cd334b
Revises: d01d118f7d4a
Create Date: 2017-11-03 11:29:50.228461

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import (
    Column, String, ForeignKey, Integer, DateTime
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import ChoiceType
from flask_sqlalchemy import SQLAlchemy


# revision identifiers, used by Alembic.
revision = '5a8606cd334b'
down_revision = 'd01d118f7d4a'
branch_labels = None
depends_on = None

db = SQLAlchemy()
Session = sessionmaker()


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

    person = relationship('Person',
                          backref=db.backref('addresses', lazy='dynamic'))


class Person(db.Model):
    """ Person model """
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)


class Entry(db.Model):
    __tablename__ = 'entry'
    id = Column(Integer, primary_key=True, autoincrement=True)
    mac_id = Column(ForeignKey('address.mac'))
    startdate = Column(DateTime, nullable=False)

    mac = relationship('Address',
                       backref=db.backref('entries', lazy='dynamic'))


def upgrade():
    op.add_column('address', sa.Column('deleted', sa.Boolean(), nullable=True,
                                       server_default=sa.false()))


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    addresses = session.query(Address).all()
    mac_addresses = []
    for address in addresses:
        mac_addresses.append({
            'mac': address.mac,
            'device': address.device,
            'person_id': address.person_id,
        })
    op.drop_table('address')
    op.create_table('address',
                    sa.Column('mac', sa.String(), primary_key=True),
                    sa.Column('device', ChoiceType(Address.DEVICES),
                              nullable=False),
                    sa.Column('person_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['person_id'], ['person.id'])
                    )
    op.bulk_insert(Address.__table__, mac_addresses)
    session.commit()
