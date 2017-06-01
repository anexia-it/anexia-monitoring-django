# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse


def access_token_check(func):
    """
    Decorator that checks if access token is set and correct before calling the method or function.

    :return: Decorator
    """
    def _is_authorized(request):

        # Access token GET param must be defined
        if 'access_token' not in request.request.GET:
            return False

        # Access token setting must be defined
        if not hasattr(settings, 'ANX_MONITORING_ACCESS_TOKEN'):
            return False

        # Validate access token
        if settings.ANX_MONITORING_ACCESS_TOKEN != request.request.GET['access_token']:
            return False

        return True

    def access_token_check_wrapper(request, *args, **kwargs):
        if not _is_authorized(request):
            return HttpResponse('401 Unauthorized', status=401)
        return func(request, *args, **kwargs)

    return access_token_check_wrapper
