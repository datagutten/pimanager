import os
import subprocess
from uuid import getnode
import pkg_resources
import requests

# json as callable was introduced in version 1.0.0
pkg_resources.require("requests>=1.0.0")


mac = getnode()
mac = ':'.join(('%012x' % mac)[i:i+2] for i in range(0, 12, 2))

if os.path.exists('/home/PiManager/url.txt'):
    with open('/home/PiManager/url.txt', 'r') as fp:
        base_url = fp.read()
        base_url = base_url.strip()
else:
    base_url = 'http://pimanager'

actions = requests.get(base_url + '/actions/'+mac)
for action in actions.json():
    print(action)
    arguments = action['command'].split(' ')
    output = ''
    requests.post(base_url + '/action_report', data={'action': action['id'],
                                                     'started': 'started'})
    try:
        output = subprocess.check_output(arguments, universal_newlines=True,
                                         stderr=subprocess.STDOUT)
        return_code = 0
    except subprocess.CalledProcessError as exception:
        return_code = exception.returncode
    except OSError as exception:
        output = exception.strerror
        return_code = 999

    print(output)

    requests.post(base_url + '/action_report', data={'action': action['id'],
                                                     'output': output,
                                                     'return_code': return_code})
