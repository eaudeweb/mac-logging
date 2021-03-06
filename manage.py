#!/usr/bin/env python

import argparse
import os.path
import sys
import re
import time

from datetime import datetime, timedelta
from flask_script import Manager, prompt, prompt_pass
from flask_security import SQLAlchemyUserDatastore, utils
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

from clocking.app import app
from clocking.models import Address, Person, Entry, User, Role, db

manager = Manager(app)
db_manager = Manager()
manager.add_command('db', db_manager)


EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def parse():
    infile = open("/var/local/pontaj/files/input.txt", "r")
    addresses = []
    for line in iter(infile):
        values = line.split(' "')
        addresses.append(values[1])

    infile.close()

    return addresses


def get_time():
    date = time.ctime(os.path.getmtime("/var/local/pontaj/files/input.txt"))
    return datetime.strptime(date, "%a %b %d %H:%M:%S %Y")


@manager.command
def check_new_entries():
    existing_addresses = [address.mac for address in
                          Address.query.filter(Address.deleted == False).all()]
    addresses = parse()
    last_modified = get_time()
    new_entries = []
    persons_ids = []
    for address in addresses:
        if address in existing_addresses:
            person_details = Person.query.join(Person.addresses).filter_by(
                mac=address
            ).first()
            if person_details.id in persons_ids:
                continue
            new_entries.append((
                address,
                person_details.last_name,
                person_details.first_name
            ))
            persons_ids.append(person_details.id)

    startdate_datetime = last_modified.replace(minute=00, hour=00, second=00)

    for address, last_name, first_name in new_entries:
        find_any_values = Entry.query.filter(
            and_(Entry.startdate >= startdate_datetime.date(),
                 Entry.startdate <= startdate_datetime.date() + timedelta(days=1))
        ).join(Entry.mac).join(Address.person).filter_by(
            last_name=last_name,
            first_name=first_name
        )
        if find_any_values.count() == 0:
            entry = Entry(**{'mac_id': address,
                             'startdate': last_modified})
            db.session.add(entry)
            db.session.commit()


@manager.command
def createsuperuser():
    email = prompt('User email')
    if not EMAIL_REGEX.match(email):
        sys.exit('\nCould not create user: Invalid E-Mail addresss')

    password = prompt_pass('User password')
    password_confirm = prompt_pass('Confirmed password')
    if not password == password_confirm:
        sys.exit('\nCould not create user: Passwords did not match')

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    user_datastore.create_user(
        email=email,
        password=utils.encrypt_password(password)
    )
    db.session.commit()
    user_datastore.add_role_to_user(email, 'superuser')
    db.session.commit()


@db_manager.option('alembic_args', nargs=argparse.REMAINDER)
def alembic(alembic_args):
    from alembic.config import CommandLine

    CommandLine().main(argv=alembic_args)


if __name__ == "__main__":
    with app.app_context():
        manager.run()
