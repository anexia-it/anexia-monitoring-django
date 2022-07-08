# -*- coding: utf-8 -*-
import asyncio
import sys

from updatable import get_package_update_list, get_parsed_environment_package_list

from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.db import connections
from django.views.generic import View
from django.conf import settings

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

    async def get_response_data(self):
        runtime = {
            'platform': 'python',
            'platform_version': sys.version,
            'framework': 'django',
            'framework_installed_version': None,
            'framework_newest_version': None,
        }
        modules = []
        packages = get_parsed_environment_package_list()

        for package in packages:
            package['_data'] = asyncio.create_task(
                get_package_update_list(package['package'], package['version'])
            )

        for package in packages:
            package_data = await package['_data']

            modules.append({
                'name': package['package'],
                'installed_version': package['version'],
                'installed_version_licences': [
                    package_data['current_release_license'],
                ],
                'newest_version': package_data['latest_release'],
                'newest_version_licences': [
                    package_data['latest_release_license'],
                ],
            })

            if package['package'] == 'Django':
                runtime['framework_installed_version'] = package['version']
                runtime['framework_newest_version'] = package_data['latest_release']

        return {
            'runtime': runtime,
            'modules': modules,
        }

    @access_token_check
    def get(self, request, *args, **kwargs):
        response = JsonResponse(asyncio.run(self.get_response_data()))
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
        if getattr(settings, 'ANX_MONITORING_TEST_DB_CONNECTIONS', True):
            for connection_key in connections:
                connections[connection_key].cursor()

        # Query for users
        if getattr(settings, 'ANX_MONITORING_TEST_QUERY_USERS', True):
            User = get_user_model()
            User.objects.all().count()

        # Registers signal for custom check
        monitor_up_check.send(sender=None)

        response = HttpResponse("OK", content_type="text/plain")
        self.add_access_control_headers(response)
        return response
