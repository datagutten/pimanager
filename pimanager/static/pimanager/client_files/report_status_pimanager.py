import re
import subprocess
from uuid import getnode
import requests

import socket
hostname = socket.gethostname()


# https://stackoverflow.com/questions/159137/getting-mac-address
mac = getnode()
mac = ':'.join(('%012x' % mac)[i:i+2] for i in range(0, 12, 2))
# print (mac)

ifconfig = subprocess.check_output(['/sbin/ip', 'addr'], universal_newlines=True)

#m = re.search('[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}', ifconfig)
#mac = m.group()

ps_aux = subprocess.check_output(['/bin/ps', 'aux'])
tvservice = subprocess.check_output(['tvservice', '-s'])
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

action = requests.post('http://pimanager/device_status/report',
                       data={'mac': mac,
                             'processes': ps_aux,
                             'ifconfig': ifconfig,
                             'hostname': hostname,
                             'tvservice': tvservice,
                             'uptime': uptime,
                             'upsince': upsince,
                             'serial': serial,
                             'model': model}
                       )
print(action.text)
