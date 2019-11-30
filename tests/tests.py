from django.test import TestCase
from pimanager.models import Device, Action


class DeviceTestCase(TestCase):
    def setUp(self):
        Device.objects.create(mac='b8:27:eb:eb:a9:dd', name='utstilling-pi-01',
                              ip='10.0.4.221',
                              monitored_process='omxplayer.bin',
                              serial='8aeba9dd',
                              number=1,
                              last_seen='2019-01-01')

    def test_last_seen_class(self):
        device = Device.objects.get(serial='8aeba9dd')
        self.assertEqual(device.last_seen_class(), 'error')
