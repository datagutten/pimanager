#!/bin/sh
# curl -s {{url}}{% url 'device_status:client_upgrade' %}|sudo sh

apt-get update
rm /home/pi/omxloop.py
rm /home/report_status_pimanager.py
rm /home/action.py
rm /media/no_media.jpg

{% include 'pimanager/client_setup.sh' with nohead='true' %}
{% include 'pimanager/omxloop_setup.sh' with nohead='true' %}