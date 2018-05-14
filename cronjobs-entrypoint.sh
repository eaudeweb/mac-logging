#!/bin/sh
set -e

echo "Running cronjobs"

echo "*/2 7-19 * * 1-5 /var/local/pontaj/crontabs/run_snmp.sh && python /var/local/pontaj/manage.py check_new_entries" > crontab.tmp

crontab crontab.tmp
rm crontab.tmp
crond -f -d 0
