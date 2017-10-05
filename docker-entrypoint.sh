#!/bin/sh
set -e

if [ ! -e files/mac_logging.db ]; then
  touch files/mac_logging.db
  ./manage.py db alembic upgrade head
  echo "Running DB CMD: ./database.py"
fi

exec ./manage.py runserver -h 0.0.0.0 -p 5000
