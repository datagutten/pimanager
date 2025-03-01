from django.core.management.base import BaseCommand

import Actions
from pimanager.models import Device


class Command(BaseCommand):
    help = 'Add action to device(s)'

    def add_arguments(self, parser):
        parser.add_argument('device', nargs='+', type=str)

    def handle(self, *args, **options):
        if not options['device'][0] == 'all':
            devices = Device.objects.filter(name=options['device'][0])
        else:
            devices = Device.objects.all()

        for device in devices:
            Actions.update_client(device)
