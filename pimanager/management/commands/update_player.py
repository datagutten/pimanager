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
            command = 'wget -O /home/pi/omxloop.py http://pimanager/static/pimanager/client_files/omxloop/omxloop.py'
            action = Action(device=device, command=command)
            action.save()
            command = 'wget -O /media/no_media.jpg http://pimanager/static/pimanager/client_files/omxloop/no_media.jpg'
            action2 = Action(device=device, command=command)
            action2.save()
