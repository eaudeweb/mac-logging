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


@manager.command
def clear_mac_addresses():
    conn = connect_to_db()
    c = conn.cursor()

    c.execute("DELETE FROM mac_addresses")
    conn.commit()

    conn.close()


def parse():
    infile = open("/var/local/pontaj/files/input.txt", "r")
    mac_addresses = []
    for line in iter(infile):
        values = line.split(' "')
        mac_addresses.append(values[1])

    infile.close()

    return mac_addresses


def get_time():
    date = time.ctime(os.path.getmtime("/var/local/pontaj/files/input.txt"))
    return datetime.strptime(date, "%a %b %d %H:%M:%S %Y")


@manager.command
def check_insert_mac_addresses():
    conn = connect_to_db()
    c = conn.cursor()

    c.execute("SELECT * FROM mac_addresses")
    existing_values = c.fetchall()
    existing_mac_addresses = [pair[1] for pair in existing_values]

    mac_addresses = parse()
    last_modified = get_time()
    c.execute("SELECT * FROM mac_addresses ORDER BY id DESC LIMIT 1")
    curr_id = c.fetchone()
    if curr_id is None:
        curr_id = 1
    else:
        curr_id = curr_id[0] + 1
    values = []
    for mac_address in mac_addresses:
        if mac_address not in existing_mac_addresses:
            values.append((curr_id, mac_address, last_modified))
            curr_id += 1

    conn.executemany("INSERT INTO mac_addresses VALUES (?, ?, ?)", values)
    conn.commit()

    conn.close()

@manager.command
def check_persons():
    conn = connect_to_db()
    c = conn.cursor()

    c.execute("SELECT * FROM mac_addresses")
    mac_addresses = c.fetchall()

    values = []
    c.execute("SELECT (id) FROM persons ORDER BY id DESC LIMIT 1")
    curr_id = c.fetchone()
    if curr_id is None:
        curr_id = 1
    else:
        curr_id = curr_id[0] + 1
    for mac_address in mac_addresses:
        c.execute("SELECT * FROM persons_mac WHERE mac = ?", (mac_address[1], ))
        persons_mac = c.fetchall()
        for person_mac in persons_mac:
            # Verify if this person is already registered for this day
            my_date = mac_address[2]
            my_date = datetime.strptime(my_date, '%Y-%m-%d %H:%M:%S')
            c.execute("SELECT * FROM persons WHERE last_name=? "
                      "AND first_name=? "
                      "AND DATE(startdate)=?", (person_mac[2], person_mac[3],
                                                my_date.date()
                                                )
                      )
            if len(c.fetchall()) == 0:
                startdate = mac_address[2]
                enddate = startdate
                enddate = datetime.strptime(enddate, '%Y-%m-%d %H:%M:%S')
                enddate += timedelta(hours=8)
                values.append((curr_id, person_mac[2], person_mac[3], startdate, enddate))
                curr_id += 1

    conn.executemany("INSERT INTO persons VALUES (?, ?, ?, ?, ?)", values)
    conn.commit()

    conn.close()


@db_manager.option('alembic_args', nargs=argparse.REMAINDER)
def alembic(alembic_args):
    from alembic.config import CommandLine

    CommandLine().main(argv=alembic_args)


if __name__ == "__main__":
    with app.app_context():
        manager.run()
