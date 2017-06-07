# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from .views import MonitorModulesView, MonitorUpView

urlpatterns = [
    # API v1
    url(r'^anxapi/v1/', include([
        url(r'^modules/$', MonitorModulesView.as_view(), name='anexia_monitor_modules'),
        url(r'^up/$', MonitorUpView.as_view(), name='anexia_monitor_up'),
    ])),
]
