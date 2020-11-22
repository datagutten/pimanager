{% load static %}
#!/bin/sh
# curl -s {{ url }}{% url 'device_status:setup' %}|sudo sh

apt-get update
apt-get -y install python3-requests python3-pkg-resources

mkdir /home/PiManager
wget -O /home/action.py {{url}}/static/pimanager/client_files/action.py
wget -O /home/report_status_pimanager.py {{url}}/static/pimanager/client_files/report_status_pimanager.py
wget -O /etc/cron.d/pimanager {{url}}/static/pimanager/client_files/pimanager.cron

/usr/bin/python3 /home/report_status_pimanager.py
/usr/bin/python3 /home/action.py

echo "{{url}}"> /home/PiManager/url.txt