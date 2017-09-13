#!/bin/sh
set -e

echo "Running cronjobs"

echo "*/2 * * * * /var/local/pontaj/crontabs/run_snmp.sh && /var/local/pontaj/crontabs/check_mac_addresses.py" >> crontab.tmp
echo "0 6 * * 1-5 /var/local/pontaj/crontabs/run_clear_macs.sh" >> crontab.tmp

crontab crontab.tmp
rm crontab.tmp
crond -f -d 0
