import os
import re
import socket
import subprocess
from uuid import getnode

import requests

hostname = socket.gethostname()

# https://stackoverflow.com/questions/159137/getting-mac-address
mac = getnode()
mac = ':'.join(('%012x' % mac)[i:i + 2] for i in range(0, 12, 2))

ifconfig = subprocess.check_output(['/sbin/ip', 'addr'], universal_newlines=True)

ps_aux = subprocess.check_output(['/bin/ps', 'aux'])

try:
    uptime = subprocess.check_output(['uptime', '-p'])
    upsince = subprocess.check_output(['uptime', '-s'])
except subprocess.CalledProcessError:
    pattern = r'.+(up.+),\s+[0-9]+ user.+'
    uptime = subprocess.check_output(['uptime'])
    uptime = re.sub(pattern, r'\1', uptime.decode('utf-8'))
    print(uptime)
    upsince = ''

with open('/proc/cpuinfo', 'r') as fp:
    cpuInfo = fp.read()

groups = re.search(r'Serial\s+: .*?([1-9a-f][0-9a-f]+)', cpuInfo)
if groups:
    serial = groups.group(1)
else:
    serial = None

with open('/sys/firmware/devicetree/base/model', 'r') as fp:
    model = fp.read()

if os.path.exists('/home/pimanager/url.txt'):
    with open('/home/pimanager/url.txt', 'r') as fp:
        url = fp.read()
        url = '%s/report' % url.strip()
else:
    url = 'http://pimanager/report'

if os.path.exists('/etc/debian_version'):
    with open('/etc/debian_version') as fp:
        debian_version = fp.read()
else:
    debian_version = None


action = requests.post(url,
                       data={'mac': mac,
                             'processes': ps_aux,
                             'ifconfig': ifconfig,
                             'hostname': hostname,
                             'tvservice': None,  # TODO: Find new way to detect screen status
                             'uptime': uptime,
                             'upsince': upsince,
                             'serial': serial,
                             'model': model,
                             'debian_version': debian_version}
                       )
print(action.text)
