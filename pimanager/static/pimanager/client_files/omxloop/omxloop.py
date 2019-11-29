#!/usr/bin/python
import subprocess
import os
import glob

path = '/media/usb/'
pidfile = open('/var/run/omxloop.pid', 'w')

# Turn off display
# subprocess.call(['tvservice', '-o'])

on = True
file_list = glob.glob(os.path.join(path, '*.mp4'))
file_list.sort()

if len(file_list) == 0:
    # Turn on display
    # subprocess.call(['tvservice', '-p'])
    cmd = ["fbi", '-a', '-fitwidth', '-t', '7', '-noverbose', '-blend', '400', '-T', '1']

    file_list_0 = glob.glob(os.path.join(path, '*.jpg'))
    file_list_1 = glob.glob(os.path.join(path, '*.png'))
    file_list_2 = glob.glob(os.path.join(path, '*.tif'))
    fl = file_list_0 + file_list_1 + file_list_2
    if len(fl) == 0:
        # https://edv-huber.com/index.php/problemloesungen/15-custom-splash-screen-for-raspberry-pi-raspbian
        subprocess.run(['fbi', '-a', '-T', '1', '-noverbose', '/media/no_media.jpg'])
    else:
        fl.sort()
        try:
            a = subprocess.call(cmd + fl)
        except KeyboardInterrupt:
            pass
else:

    sub_list = [None] * len(file_list)
    for idx, infile in enumerate(file_list):
        bname = os.path.splitext(infile)[0]
        if os.path.exists(bname + '.srt'):
            sub_list[idx] = bname + '.srt'

    # Turn on display
    subprocess.call(['tvservice', '-p'])
    while on:
        for idx, infile in enumerate(file_list):
            try:
                if sub_list[idx] is not None:
                    args = ["omxplayer", '--subtitles', sub_list[idx], infile]
                else:
                    args = ["omxplayer", infile]
                a = subprocess.call(args)
            except KeyboardInterrupt:
                on = False
                break
