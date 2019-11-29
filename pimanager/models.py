from django.db import models
from datetime import datetime
from django.apps import apps


class Device(models.Model):
    mac = models.CharField(max_length=45, unique=True)
    name = models.CharField('Navn', max_length=200, blank=True, null=True)
    description = models.CharField('Beskrivelse', max_length=200, blank=True, null=True)
    message = models.CharField(max_length=200, blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    last_seen = models.DateTimeField('Sist sett', auto_now=False, blank=True, null=True)
    number = models.IntegerField('Nummer', blank=True, null=True)
    monitored_process = models.CharField(max_length=200, blank=True, null=True)
    uptime = models.CharField('Oppetid', max_length=200, blank=True, null=True)
    screen_status = models.CharField('Skjermstatus', max_length=200, blank=True, null=True)
    serial = models.CharField(max_length=50, blank=True, null=True,
                              unique=True,
                              verbose_name='Serienummer')
    model = models.CharField('Modell', max_length=200, blank=True, null=True)
    hide = models.BooleanField('Skjul', default=False)

    def __str__(self):
        return str(self.ip) + ' ' + str(self.name) + ' ' + str(self.description)

    class Meta:
        ordering = ['number']

    def interface(self):
        if apps.is_installed('switchinfo'):
            from switchinfo.models import Mac
            mac_address = self.mac.replace(':', '')
            mac = Mac.objects.get(mac=mac_address)
            if Mac.objects.filter(interface=mac.interface).count() > 1:
                return None
            else:
                return mac.interface

    def port(self):
        if apps.is_installed('switchinfo'):
            from switchinfo.models import Mac
            mac_address = self.mac.replace(':', '')
            mac = Mac.objects.get(mac=mac_address)
            return '%s %s' % (mac.interface.switch.name, mac.interface)

    def last_seen_class(self):
        if self.last_seen is None:
            return 'good'
        diff = datetime.today()-self.last_seen

        if diff.days > 0:
            return 'error'
        elif diff.seconds < 60*15:
            return 'good'
        elif diff.seconds < 3600*24:
            return 'warning'

        return diff.seconds

    def pending_actions(self):
        actions = Action.objects.filter(device=self, executed=None)
        return actions


class Action(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    command = models.CharField(max_length=200)
    added = models.DateTimeField(auto_now_add=True)
    executed = models.DateTimeField(auto_now=False, blank=True, null=True)
    return_code = models.IntegerField(blank=True, null=True)
    output = models.TextField(blank=True, null=True)
