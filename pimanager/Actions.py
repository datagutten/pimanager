from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, \
    render as django_render
from django.views.decorators.csrf import csrf_exempt

from pimanager.models import Action, Device

try:
    from config_backup import ConfigBackup
except ImportError:
    pass


def power_cycle(device):
    if apps.is_installed('config_backup'):

        device = Device.objects.get(serial=device)
        interface = device.interface
        options = ConfigBackup.backup_options(interface.switch)
        if options.connection_type == 'SSH' or \
                options.connection_type == 'Telnet':
            cli = ConfigBackup.connect(interface.switch,
                                       options.connection_type)
        else:
            cli = ConfigBackup.connect(interface.switch)

        if interface.switch.type == 'Cisco':
            output = cli.command('conf t', 'config')
            output += cli.command('in %s' % interface, 'config-if')
            output += cli.command('power inline never', 'config-if')
            output += cli.command('power inline auto', 'config-if')
            output += cli.command('exit', 'config')
            output += cli.command('exit', '#')

            return output
        else:
            return 'Unable to power cycle, %s is not supported' % interface.switch.type
    else:
        return 'Unable to power cycle, config_backup is not installed'
