from django.core.management.base import BaseCommand

from pimanager.models import Action, Device
from django.conf import settings


class Command(BaseCommand):
    help = 'Add action to device(s)'

    def add_arguments(self, parser):
        parser.add_argument('device', nargs='+', type=str)

    def handle(self, *args, **options):
        if not options['device'][0] == 'all':
            devices = Device.objects.filter(name=options['device'][0])
        else:
            devices = Device.objects.all()

        try:
            url = settings.SITE_URL
        except AttributeError:
            url = 'http://pimanager'

        for device in devices:
            Action(device=device,
                   command='wget -O /home/pimanager_upgrade.sh %s/upgrade' %
                           url).save()
            Action(device=device,
                   command='sh /home/pimanager_upgrade.sh').save()
            Action(device=device,
                   command='rm /home/pimanager_upgrade.sh').save()
