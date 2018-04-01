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

# Update Postgres sequences.
psql $PG_DB_NAME $PG_USER_NAME -c "\ds" | grep sequence | cut -d'|' -f2 | tr -d '[:blank:]' |
while read sequence_name; do
  table_name=${sequence_name%_id_seq}

  psql $PG_DB_NAME $PG_USER_NAME -c "select setval('$sequence_name', (select max(id) from $table_name))"
done
