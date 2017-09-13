#!/usr/bin/env python

import datetime
import sqlite3
from datetime import datetime
import os.path
import time


def connect_to_db():
    return sqlite3.connect("/var/local/pontaj/files/mac_logging.db")


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


def check_insert_mac_addresses():
    conn = connect_to_db()
    c = conn.cursor()

    c.execute("SELECT * FROM mac_addresses")
    existing_values = c.fetchall()
    existing_mac_addresses = [pair[1] for pair in existing_values]

    mac_addresses = parse()
    last_modified = get_time()
    curr_id = len(existing_mac_addresses)
    values = []
    for mac_address in mac_addresses:
        if mac_address not in existing_mac_addresses:
            values.append((curr_id, mac_address, last_modified))
            curr_id += 1

    conn.executemany("INSERT INTO mac_addresses VALUES (?, ?, ?)", values)
    conn.commit()

    conn.close()


check_insert_mac_addresses()
