{% load static %}
{% if not nohead %}
#!/bin/sh
# curl -s {{url}}{% url 'device_status:setup_omxloop' %}|sudo sh

apt-get update
{% endif %}
apt-get -y install omxplayer fbi

mkdir /home/pi/omxloop
wget -O /home/pi/omxloop/omxloop.py {{url}}{% static 'pimanager/omxloop/omxloop.py' %}
chmod +x /home/pi/omxloop/omxloop.py
wget -O /etc/init.d/omxloop {{url}}{% static 'pimanager/omxloop/omxloop_init.sh' %}
chmod +x /etc/init.d/omxloop
update-rc.d omxloop defaults
wget -O /home/pi/omxloop/no_media.jpg {{url}}{% static 'pimanager/omxloop/no_media.jpg' %}

/etc/init.d/omxloop start
