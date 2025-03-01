from django.apps import apps
from django.conf import settings

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


def update_client(device: Device):
    Action(device=device,
           command='wget -O /home/pimanager_upgrade.sh %s/upgrade' %
                   settings.base_url).save()
    Action(device=device,
           command='sh /home/pimanager_upgrade.sh').save()
    Action(device=device,
           command='rm /home/pimanager_upgrade.sh').save()
