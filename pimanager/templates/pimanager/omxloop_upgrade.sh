#!/bin/sh
# curl -s {{url}}{% url 'device_status:omxloop_upgrade' %}|sudo sh

apt-get update

rm /home/pi/omxloop.py
rm /media/no_media.jpg

{% include 'pimanager/omxloop_setup.sh' with nohead='true' %}