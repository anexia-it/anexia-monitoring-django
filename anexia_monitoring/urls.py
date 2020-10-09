# -*- coding: utf-8 -*-
from django.urls import include, re_path

from .views import MonitorModulesView, MonitorUpView

urlpatterns = [
    # API v1
    re_path(r'^anxapi/v1/', include([
        re_path(r'^modules/$', MonitorModulesView.as_view(), name='anexia_monitor_modules'),
        re_path(r'^up/$', MonitorUpView.as_view(), name='anexia_monitor_up'),
    ])),
]
