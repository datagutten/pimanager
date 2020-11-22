from django.core.management.base import BaseCommand
from django.urls import reverse

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
            command = 'wget -O /tmp/client_setup.sh %s%s' % (url, reverse('device_status:setup'))
            action = Action(device=device, command=command)
            action.save()
            command = 'sh /tmp/client_setup.sh'
            action2 = Action(device=device, command=command)
            action2.save()
