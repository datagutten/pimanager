#!/bin/sh
# curl -s http://pimanager/static/pimanager/client_scripts/omxloop_setup.sh|sudo sh
wget -O /home/pi/omxloop.py http://pimanager/static/pimanager/client_files/omxloop/omxloop.py
chmod +x /home/pi/omxloop.py
wget -O /etc/init.d/omxloop http://pimanager/static/pimanager/client_files/omxloop/omxloop_init.sh
chmod +x /etc/init.d/omxloop
update-rc.d omxloop defaults
wget -O /media/no_media.jpg http://pimanager/static/pimanager/client_files/omxloop/no_media.jpg

/etc/init.d/omxloop start