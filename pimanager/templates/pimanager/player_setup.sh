{% load static %}
{% if not nohead %}
#!/bin/sh
# curl -s {{url}}{% url 'device_status:setup_player' %}|sh

apt-get update
{% endif %}
apt-get -y install vlc fbi

mkdir /home/player/player
wget -O /home/player/player/video_loop.py {{url}}{% static 'pimanager/omxloop/video_loop.py' %}
chmod +x /home/player/player/video_loop.py
wget -O /etc/init.d/video_loop {{url}}{% static 'pimanager/omxloop/video_loop_init.sh' %}
chmod +x /etc/init.d/video_loop
update-rc.d video_loop defaults
wget -O /home/player/player/no_media.jpg {{url}}{% static 'pimanager/omxloop/no_media.jpg' %}

touch /var/log/video_loop.log
chown player /var/log/video_loop.log

/etc/init.d/video_loop start
