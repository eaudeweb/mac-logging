#!/usr/bin/env python

import sqlite3


def connect_to_db():
    return sqlite3.connect("/home/catalin/Workspace/mac-logging/mac_logging.db")


def clear_mac_addresses():
    conn = connect_to_db()
    c = conn.cursor()

    c.execute("DELETE FROM mac_addresses")
    conn.commit()

    conn.close()


clear_mac_addresses()
