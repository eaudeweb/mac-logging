#!/bin/sh

SQLITE_DUMP_FILE=$1
PG_DB_NAME=$2
PG_USER_NAME=$3

# PRAGMAs are specific to SQLite3.
sed -i '/PRAGMA/d' $SQLITE_DUMP_FILE
# Convert sequences.
sed -i '/sqlite_sequence/d ; s/integer PRIMARY KEY AUTOINCREMENT/serial PRIMARY KEY/ig' $SQLITE_DUMP_FILE
# Convert column types.
sed -i 's/DATETIME/TIMESTAMP/g ; s/integer[(][^)]*[)]/integer/g ; s/text[(]\([^)]*\)[)]/varchar(\1)/g' $SQLITE_DUMP_FILE

sed -i '/sqlite_sequence/d ; s/integer NOT NULL PRIMARY KEY AUTOINCREMENT/serial NOT NULL PRIMARY KEY/ig' $SQLITE_DUMP_FILE

sed -i -- 's/deleted BOOLEAN DEFAULT 0/deleted BOOLEAN DEFAULT FALSE/g' $SQLITE_DUMP_FILE

sed -i -r -- 's/INSERT INTO address VALUES\((.*),(.*),(.*),0\)/INSERT INTO address VALUES(\1,\2,\3,FALSE)/g' $SQLITE_DUMP_FILE

#createdb -U $PG_USER_NAME $PG_DB_NAME
psql $PG_DB_NAME $PG_USER_NAME < $SQLITE_DUMP_FILE

# Create sequences
psql $PG_DB_NAME $PG_USER_NAME -c "CREATE SEQUENCE person_id_seq;"
psql $PG_DB_NAME $PG_USER_NAME -c "CREATE SEQUENCE address_id_seq;"
psql $PG_DB_NAME $PG_USER_NAME -c "CREATE SEQUENCE entry_id_seq;"


# Update Postgres sequences.
psql $PG_DB_NAME $PG_USER_NAME -c "select setval('person_id_seq', (select max(id) from person))"
psql $PG_DB_NAME $PG_USER_NAME -c "select setval('entry_id_seq', (select max(id) from entry))"

psql $PG_DB_NAME $PG_USER_NAME -c "ALTER TABLE person ALTER id SET DEFAULT NEXTVAL('person_id_seq')"
psql $PG_DB_NAME $PG_USER_NAME -c "ALTER TABLE entry ALTER id SET DEFAULT NEXTVAL('entry_id_seq')"
