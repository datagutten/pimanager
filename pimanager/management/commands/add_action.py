from django.core.management.base import BaseCommand

from pimanager.models import Action, Device


class Command(BaseCommand):
    help = 'Add action to device(s)'

    def add_arguments(self, parser):
        parser.add_argument('device', nargs='+', type=str)
        parser.add_argument('command', nargs='+', type=str)        

    def handle(self, *args, **options):
        if not options['device'][0] == 'all':
            devices = Device.objects.filter(name=options['device'][0])
        else:
            devices = Device.objects.all()
        for device in devices:
            action = Action(device=device, command=options['command'][0])
            action.save()
