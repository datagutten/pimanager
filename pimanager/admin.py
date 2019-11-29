from django.contrib import admin

# Register your models here.

from .models import Action, Device


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'mac', 'ip', 'last_seen', 'serial')


admin.site.register(Device, DeviceAdmin)


class ActionAdmin(admin.ModelAdmin):
    list_display = ('device', 'command', 'added', 'executed', 'return_code')
    list_filter = ('device', 'return_code')


admin.site.register(Action, ActionAdmin)
