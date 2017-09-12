#!/bin/sh
set -e

if [ ! -e mac_logging.db ]; then
  touch mac_logging.db
  echo "Running DB CMD: ./database.py"
  python database.py
fi

exec python app.py