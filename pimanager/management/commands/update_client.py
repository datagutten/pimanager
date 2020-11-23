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
            command = 'wget -O /home/action.py %s/static/' \
                      'pimanager/client_files/action.py' % url
            action = Action(device=device, command=command)
            action.save()

            command = 'wget -O /home/report_status_pimanager.py %s/static/' \
                      'pimanager/client_files/report_status_pimanager.py' % url
            action2 = Action(device=device, command=command)
            action2.save()
