#!/usr/bin/python
import subprocess
import os
import glob

media_path = '/media/usb/'

video_extensions = ['mp4', 'mkv']
image_extensions = ['jpg', 'png', 'tif', 'tiff']
image_time = 7

on = True
script_path = os.path.dirname(os.path.realpath(__file__))
media_path = os.path.realpath(media_path)


def find_player():
    for player_iter in ['omxplayer', 'vlc']:
        check = subprocess.run(['which', player_iter])
        if check.returncode == 0:
            return player_iter

    raise RuntimeError('No supported player found')


def build_file_list(file_path: str, extensions: list) -> list:
    file_list = []
    for extension in extensions:
        file_list += glob.glob(os.path.join(file_path, '*.%s' % extension))

    file_list.sort()
    return file_list


video_list = build_file_list(media_path, video_extensions)

if len(video_list) == 0:
    image_list = build_file_list(media_path, image_extensions)

    if len(image_list) == 0:
        # https://edv-huber.com/index.php/problemloesungen/15-custom-splash-screen-for-raspberry-pi-raspbian
        subprocess.run(
            ['fbi', '-a', '-T', '1', '-noverbose', os.path.join(script_path, 'no_media.jpg')])
    else:
        try:
            cmd = ["fbi", '-a', '-fitwidth', '-t', image_time, '-noverbose', '-blend', '400', '-T',
                   '1']
            a = subprocess.call(cmd + image_list)
        except KeyboardInterrupt:
            pass
else:
    player = find_player()

    while on:
        try:
            if player == 'vlc':
                args = ['cvlc', '-f', '--video-on-top', '--loop']
                args += video_list
                status = subprocess.run(args)
                status.check_returncode()
            else:
                for idx, infile in enumerate(video_list):
                    basename = os.path.splitext(infile)[0]
                    if os.path.exists(basename + '.srt'):
                        sub_file = basename + '.srt'
                    else:
                        sub_file = None

                        if player == 'omxplayer':
                            if sub_file:
                                args = ["omxplayer", '--subtitles', sub_file, infile]
                            else:
                                args = ["omxplayer", infile]
                        else:
                            raise RuntimeError('No supported player found')

                        status = subprocess.run(args)
                        status.check_returncode()

        except KeyboardInterrupt:
            on = False
            break
