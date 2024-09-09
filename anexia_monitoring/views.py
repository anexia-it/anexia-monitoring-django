import asyncio
import sys

from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.db import connections
from django.dispatch import receiver
from django.views.generic import View
from django.conf import settings

from .core import get_python_env_info
from .decorators import access_token_check
from .events import monitor_up_check


class BaseView(View):
    """
    Base view
    """

    @staticmethod
    def add_access_control_headers(response):
        """
        Adds CORS headers to http response

        :param response: HttpResponse
        :return: HttpResponse
        """
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        return response

    def options(self, request, *args, **kwargs):
        response = HttpResponse()
        self.add_access_control_headers(response)
        return response


class MonitorModulesView(BaseView):
    """
    A view that returns a list of all modules installed on the current environment, having current and latest version
    of the module. It also contains information about the runtime (python and django version).
    """

    @access_token_check
    def get(self, request, *args, **kwargs):
        response = JsonResponse(asyncio.run(get_python_env_info()))
        self.add_access_control_headers(response)
        return response


class MonitorUpView(BaseView):
    """
    Simple view that checks if the Django is alive and working correctly

    Checks for:
      - Database connections
      - Query for users
      - Registers signal for custom check
    """

    @access_token_check
    def get(self, request, *args, **kwargs):
        response_contents = []
        response_status = 200

        # Sends signal for health check implementations
        up_check_results = monitor_up_check.send_robust(sender=None)
        up_check_result_warnings = [
            r[1] for r in up_check_results
            if isinstance(r[1], Exception) and getattr(r[1], "is_anx_monitoring_up_warning", False)
        ]
        up_check_result_errors = [
            r[1]
            for r in up_check_results
            if isinstance(r[1], Exception) and not getattr(r[1], "is_anx_monitoring_up_warning", False)
        ]

        if not up_check_result_warnings and not up_check_result_errors:
            response_contents.append("OK")
            response_status = 200

        for up_check_result_warning in up_check_result_warnings:
            response_contents.append("WARNING: {}".format(str(up_check_result_warning) or "-"))
            response_status = 200

        for up_check_result_error in up_check_result_errors:
            response_contents.append("ERROR: {}".format(str(up_check_result_error) or "-"))
            response_status = 500

        response = HttpResponse("\n".join(response_contents), content_type="text/plain", status=response_status)
        self.add_access_control_headers(response)
        return response


if getattr(settings, 'ANX_MONITORING_TEST_DB_CONNECTIONS', True):
    @receiver(monitor_up_check)
    def anx_monitoring_test_db_connections(sender, **kwargs):
        for connection_key in connections:
            connections[connection_key].cursor()

if getattr(settings, 'ANX_MONITORING_TEST_QUERY_USERS', True):
    @receiver(monitor_up_check)
    def anx_monitoring_test_query_users(sender, **kwargs):
        user_model = get_user_model()
        user_model.objects.all().count()
