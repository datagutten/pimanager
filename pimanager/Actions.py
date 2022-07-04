from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, \
    render as django_render
from django.views.decorators.csrf import csrf_exempt

from pimanager.models import Action, Device

try:
    from config_backup import ConfigBackup
    from config_backup.switch_cli.connections.exceptions import UnexpectedResponse
except ImportError:
    pass


def power_cycle(device):
    if apps.is_installed('config_backup'):

        device = Device.objects.get(serial=device)
        interface = device.interface
        options = ConfigBackup.backup_options(interface.switch)

        if options is None:
            return

        cli = ConfigBackup.connect_cli(device.interface.switch)
        try:
            output = cli.poe_off(device.interface.interface)
            output += cli.poe_on(device.interface.interface)
        except NotImplementedError:
            return 'Power cycling on %s is not supported' % device.interface.switch.type
        except UnexpectedResponse as e:
            return str(e)

        return output

    else:
        return 'Unable to power cycle, config_backup is not installed'
