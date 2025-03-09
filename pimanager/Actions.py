from django.apps import apps
from django.conf import settings

from pimanager.models import Action, Device


def power_cycle(serial: str) -> str:
    if apps.is_installed('config_backup'):
        import config_backup.exceptions
        from config_backup import ConfigBackup
        from config_backup.switch_cli.connections.exceptions import UnexpectedResponse
        device = Device.objects.get(serial=serial)

        try:
            cli = ConfigBackup.connect(device.interface.switch)
            output = cli.poe_off(device.interface.interface)
            output += cli.poe_on(device.interface.interface)
            output = output.decode()
        except NotImplementedError:
            return 'Power cycling on %s is not supported' % device.interface.switch.type
        except UnexpectedResponse as e:
            return str(e) + str(e.payload)
        except config_backup.exceptions.BackupException as e:
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
