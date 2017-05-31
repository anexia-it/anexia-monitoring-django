from django.conf.urls import url, include

from .views import monitor_modules_view, monitor_up_view

urlpatterns = [
    # API v1
    url(r'^anxapi/v1/', include([
        url(r'^modules/$', monitor_modules_view, name='anexia_monitor_modules'),
        url(r'^up/$', monitor_up_view, name='anexia_monitor_up'),
    ])),
]
