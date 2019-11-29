from django.core.management.base import BaseCommand

from pimanager.models import Action, Device


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
            command = 'wget -O /tmp/client_setup.sh http://pimanager/static/pimanager/client_scripts/client_setup.sh'
            action = Action(device=device, command=command)
            action.save()
            command = 'sh /tmp/client_setup.sh'
            action2 = Action(device=device, command=command)
            action2.save()
