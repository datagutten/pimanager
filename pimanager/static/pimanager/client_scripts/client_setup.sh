#!/bin/sh
# curl -s http://pimanager/static/pimanager/client_scripts/client_setup.sh|sudo sh

apt-get update
apt-get -y install python3-requests python3-pkg-resources


wget -O /home/action.py http://pimanager/static/client_files/action.py
wget -O /home/report_status_pimanager.py http://pimanager/static/client_files/report_status_pimanager.py
wget -O /etc/cron.d/pimanager http://pimanager/static/client_files/pimanager.cron

/usr/bin/python3 /home/report_status_pimanager.py
/usr/bin/python3 /home/action.py
