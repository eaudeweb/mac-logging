#!/bin/sh
set -e

if [ ! -e files/mac_logging.db ]; then
  touch files/mac_logging.db
  echo "Running DB CMD: ./database.py"
fi

exec python app.py
