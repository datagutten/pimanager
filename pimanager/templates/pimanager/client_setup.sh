{% load static %}
{% if not nohead %}
#!/bin/sh
# curl -s {{ url }}{% url 'device_status:setup' %}|sudo sh

apt-get update
{% endif %}
apt-get -y install python3-requests python3-pkg-resources

mkdir /home/pimanager
mkdir /var/log/pimanager

wget -O /home/pimanager/action.py {{url}}{% static 'pimanager/client/action.py' %}
wget -O /home/pimanager/report_status.py {{url}}{% static 'pimanager/client/report_status.py' %}
wget -O /etc/cron.d/pimanager {{url}}{% static 'pimanager/client_files/pimanager.cron' %}

echo "{{url}}" >/home/pimanager/url.txt

/usr/bin/python3 /home/pimanager/report_status.py
/usr/bin/python3 /home/pimanager/action.py
