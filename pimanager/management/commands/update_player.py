from django.core.management.base import BaseCommand

from pimanager.models import Action, Device


class Command(BaseCommand):
    help = 'Update player on device(s)'

    def add_arguments(self, parser):
        parser.add_argument('device', nargs='+', type=str)

    def handle(self, *args, **options):
        if not options['device'][0] == 'all':
            devices = Device.objects.filter(name=options['device'][0])
        else:
            devices = Device.objects.all()
        for device in devices:
            commands = [
                'wget -O player_setup.sh http://pimanager/player',
                'sh player_setup.sh'
            ]
            for command in commands:
                action = Action(device=device, command=command)
                action.save()
