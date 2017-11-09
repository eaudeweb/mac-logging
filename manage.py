#!/usr/bin/env python

import argparse
import datetime
import os.path
import sqlite3
import time
from datetime import datetime, timedelta

from flask_script import Manager

from clocking.app import app


manager = Manager(app)
db_manager = Manager()
manager.add_command('db', db_manager)


def connect_to_db():
    return sqlite3.connect("/var/local/pontaj/files/mac_logging.db")


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
    conn = connect_to_db()
    c = conn.cursor()

    c.execute("SELECT * FROM address WHERE address.deleted=0")
    existing_values = c.fetchall()
    existing_addresses = [x[0] for x in existing_values]

    addresses = parse()
    last_modified = get_time()
    new_entries = []
    for address in addresses:
        if address in existing_addresses:
            c.execute("SELECT * FROM person JOIN address "
                      "ON address.person_id = person.id "
                      "AND address.mac=?", (address, ))
            person_details = c.fetchone()
            new_entries.append((address, person_details[1], person_details[2]))

    c.execute("SELECT (id) FROM entry ORDER BY id DESC LIMIT 1")
    curr_id = c.fetchone()
    if curr_id is None:
        curr_id = 1
    else:
        curr_id = curr_id[0] + 1

    values = []

    startdate_datetime = last_modified
    startdate_string = datetime.strftime(startdate_datetime, '%Y-%m-%d %H:%M:%S')
    for new_entry in new_entries:
        c.execute("SELECT * FROM address a JOIN entry e ON a.mac = e.mac_id "
                  "JOIN person p ON p.id = a.person_id "
                  "WHERE p.last_name=? "
                  "AND p.first_name=? "
                  "AND DATE(e.startdate)=?", (new_entry[1], new_entry[2], startdate_datetime.date()))
        if len(c.fetchall()) == 0:
            values.append((curr_id, new_entry[0], startdate_string))
            curr_id += 1

    conn.executemany("INSERT INTO entry VALUES (?, ?, ?)", values)
    conn.commit()

    conn.close()


@db_manager.option('alembic_args', nargs=argparse.REMAINDER)
def alembic(alembic_args):
    from alembic.config import CommandLine

    CommandLine().main(argv=alembic_args)


if __name__ == "__main__":
    with app.app_context():
        manager.run()
