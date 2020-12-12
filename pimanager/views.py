import datetime
import os
import re
from pprint import pprint

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render as django_render
from django.views.decorators.csrf import csrf_exempt

from pimanager.models import Action, Device


def render(request, template_name, context=None, content_type=None, status=None, using=None):
    version_file = os.path.join(apps.get_app_config('pimanager').path, 'VERSION')
    if os.path.exists(version_file):
        with open(version_file) as fp:
            version = fp.read().strip()
        version = version
        context['version'] = version
    else:
        context['version'] = 'development version'

    return django_render(request, template_name, context, content_type, status, using)


@csrf_exempt
def report(request):
    if request.method == "POST":
        number = re.match(r'.+pi\-([0-9]+)', request.POST['hostname'])

        if 'serial' not in request.POST:
            return HttpResponse('Missing serial number')
        dev, new = Device.objects.get_or_create(serial=request.POST['serial'],
                                                defaults={'name': request.POST['hostname'],
                                                          'ip': request.META['REMOTE_ADDR']})
        if number:
            dev.number = int(number.group(1))
        pprint(dev)
        dev.name = request.POST['hostname']
        if 'serial' in request.POST:
            dev.serial = request.POST['serial']
        if 'uptime' in request.POST:
            dev.uptime = request.POST['uptime']
        if 'tvservice' in request.POST:
            dev.screen_status = request.POST['tvservice']
        if 'model' in request.POST:
            dev.model = request.POST['model']
        if 'mac' in request.POST:
            dev.mac = request.POST['mac']
            try:
                dev.interface = dev.find_interface()
            except ObjectDoesNotExist:
                pass

        dev.ip = request.META['REMOTE_ADDR']
        dev.last_seen = datetime.datetime.now()

        if dev.monitored_process:
            if 'processes' in request.POST:
                process = re.search(r'.+%s (.+)' % dev.monitored_process, request.POST['processes'])
                if process:
                    if dev.monitored_process == 'omxplayer.bin':
                        dev.message = 'Playing %s' % process.group(1)
                    elif dev.monitored_process == 'chromium-browser':
                        dev.message = '%s running' % dev.monitored_process
                    elif dev.monitored_process == 'fbi':
                        dev.message = '%s running' % dev.monitored_process
                    else:
                        dev.message = '%s running with argument %s' % (dev.monitored_process, process.group(1))
                else:
                    dev.message = '%s not found' % dev.monitored_process

        dev.save()
        if not new:
            return HttpResponse('Updated status for device %s %s' % (dev.number, datetime.datetime.now()))
        else:
            return HttpResponse('Added new device %s %s' % (dev.number, datetime.datetime.now()))

    else:
        return HttpResponse('Not a POST request')


def device_list(request, show_all=False):
    if not show_all:
        devices = Device.objects.filter(hide=False).order_by('number')
    else:
        devices = Device.objects.order_by('number')
    context = {
        'devices': devices,
    }
    return render(request, 'pimanager/devices.html', context)


def device_list_all(request):
    return device_list(request, True)


def actions_json(request, mac):
    device = get_object_or_404(Device, mac=mac)
    actions = Action.objects.filter(device=device, executed=None)

    return JsonResponse(list(actions.values()), safe=False)


def action_list(request, mac=None, serial=None, pending=True):
    if mac:
        actions = Action.objects.filter(device__mac=mac)
    elif serial:
        actions = Action.objects.filter(device__serial=serial)
    else:
        actions = Action.objects.all()
    if pending:
        actions.filter(executed=None)

    context = {'actions': actions}
    return render(request, 'pimanager/actions.html', context)


@csrf_exempt
def action_report(request):
    if request.method == "POST":
        action = get_object_or_404(Action, id=request.POST['action'])
        if 'started' in request.POST:
            action.executed = datetime.datetime.now()
        else:
            action.output = request.POST['output']
            action.return_code = request.POST['return_code']

        action.save()
    return HttpResponse('ok')


def tv_off(request, device):
    command = 'tvservice -o'
    action = Action(device=device, command=command)
    action.save()
    return redirect('device_status:action_list')


def reboot(request, device):
    command = 'reboot'
    action = Action(device=device, command=command)
    action.save()


def client_setup(request):
    host = request.build_absolute_uri('/')[:-1]
    return render(request, 'pimanager/client_setup.sh', {'url': host})


def power_cycle(request, device):
    # TODO: Integrate with switch backup
    return HttpResponse('Power cycle not implemented')
