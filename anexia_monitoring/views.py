# -*- coding: utf-8 -*-
import sys
from updatable import get_package_update_list, get_parsed_environment_package_list

from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.db import connections
from django.views.generic import View

from .decorators import access_token_check
from .events import monitor_up_check

User = get_user_model()


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
    of the module. It also contains information about the platform (python and django version).
    """

    @access_token_check
    def get(self, request, *args, **kwargs):
        modules = []
        packages = get_parsed_environment_package_list()

        for package in packages:
            package_data = get_package_update_list(package['package'], package['version'])

            if package['package'] == 'Django':
                django_data = {
                    'installed_version': package['version'],
                    'newest_version': package_data['latest_release'],
                }
            else:
                modules.append({
                    'name': package['package'],
                    'installed_version': package['version'],
                    'newest_version': package_data['latest_release'],
                })

        platform = {
            'platform': 'python',
            'platform_version': sys.version,
            'framework': 'django',
            'framework_installed_version': django_data['installed_version'],
            'framework_newest_version': django_data['newest_version'],
        }

        data = {
            'platform': platform,
            'modules': modules,
        }

        response = JsonResponse(data)
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
        # Test database connections
        for connection_key in connections:
            connections[connection_key].cursor()

        # Query for users
        User.objects.all().count()

        # Registers signal for custom check
        monitor_up_check.send(sender=None)

        response = HttpResponse("OK", content_type="text/plain")
        self.add_access_control_headers(response)
        return response
