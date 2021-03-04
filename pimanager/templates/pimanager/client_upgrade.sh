#!/bin/sh
# curl -s {{url}}{% url 'device_status:client_upgrade' %}|sudo sh

apt-get update

rm /home/report_status_pimanager.py
rm /home/action.py

{% include 'pimanager/client_setup.sh' with nohead='true' %}