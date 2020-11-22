from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'device_status'
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.device_list, name='index'),
    path('all', views.device_list_all, name='index'),
    path('device_status/', views.device_list, name='status'),
    path('device_status/report', views.report, name='report'),
    path('report', views.report, name='report'),
    path('devices', views.device_list, name='devices'),
    path('actions/<str:mac>', views.actions_json, name='actions'),
    path('actions/<str:mac>/pending', views.action_list, name='actions_pending'),
    path('actions', views.action_list, name='action_list'),
    path('action_report', views.action_report, name='action_report'),
    path('power_cycle/<str:device>', views.power_cycle, name='power_cycle_device'),
    path('setup', views.client_setup, name='setup'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
