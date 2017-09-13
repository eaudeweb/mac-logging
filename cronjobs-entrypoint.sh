#!/bin/sh
set -e

echo "Running cronjobs"

echo "*/2 * * * * /var/local/pontaj/crontabs/run_snmp.sh && python /var/local/pontaj/manage.py check_insert_mac_addresses" >> crontab.tmp
echo "0 6 * * 1-5 python /var/local/pontaj/manage.py clear_mac_addresses" >> crontab.tmp

crontab crontab.tmp
rm crontab.tmp
crond -f -d 0
