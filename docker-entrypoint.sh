#!/bin/sh
set -e

if [ ! -e files/mac_logging.db ]; then
  touch files/mac_logging.db
  echo "Running DB CMD: ./database.py"
fi

exec python manage.py runserver -h 0.0.0.0 -p 5000
