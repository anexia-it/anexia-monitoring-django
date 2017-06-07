Anexia monitoring
=================

A Django app used to monitor updates for Django and all installed python
packages in the running environment.
It can be also used to check if the website is alive and working
correctly.

Installation and configuration
------------------------------

Install the package by using pip

::

  pip install anexia-monitoring

Add the app the settings installed apps

::

 INSTALLED_APPS = [
    ...
    # Anexia monitor
    'anexia_monitoring',
    ...
  ]

In the projects settings.py add the access token configuration:

::

  ANX_MONITORING_ACCESS_TOKEN = 'custom_access_token'

Add URL configuration for REST endpoint

::

 from anexia_monitoring import urls as monitor_urls
  ...
  urlpatterns = [
    ...
    # Anexia monitoring
    url(r'^', include(monitor_urls)),
    ...
]

Usage
-----

The plugin registers some custom REST endpoints which can be used for
monitoring. Make sure that the **ANX\_MONITORING\_ACCESS\_TOKEN** is
defined, since this is used for authorization. The endpoints will return
a 401 HTTP\_STATUS code if the token is not define or invalid, and a
200 status code otherwise.

Version monitoring
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns all a list with platform and module information.

**URL:** ``/anxapi/v1/modules/?access_token=custom_access_token``

Response headers:

::

 Status Code: 200 OK
  Access-Control-Allow-Origin: *
  Access-Control-Allow-Credentials: true
  Allow: GET
  Content-Type: application/json

Response body:

::

  {
     "platform":{
        "platform":"python",
        "framework_installed_version":"1.11.1",
        "framework_newest_version":"1.11.2",
        "framework":"django",
        "platform_version":"3.5.3 (default, Apr 26 2017, 20:12:19) \n[GCC 4.9.2]"
     },
     "modules":[
        {
           "newest_version":"0.7.10",
           "name":"alabaster",
           "installed_version":"0.7.10"
        },
        {
           "newest_version":"1.4.3",
           "name":"appdirs",
           "installed_version":"1.4.3"
        },
        {
           "newest_version":"0.22.0",
           "name":"asn1crypto",
           "installed_version":"0.22.0"
        },
        {
           "newest_version":"2.4.0",
           "name":"Babel",
           "installed_version":"2.4.0"
        },
        {
           "newest_version":"1.10.0",
           "name":"cffi",
           "installed_version":"1.10.0"
        },
        {
           "newest_version":"0.7.3",
           "name":"CommonMark",
           "installed_version":"0.5.4"
        }
     ]
  }

Live monitoring
^^^^^^^^^^^^^^^

This endpoint can be used to verify if the application is alive and
working correctly. It checks if the database connection is working and
makes a query for users. It allows to register custom checks by using
the dispatched **monitor_up_check** event.

**URL:** ``/anxapi/v1/up/?access_token=custom_access_token``

Response headers:

::

 Status Code: 200 OK
  Access-Control-Allow-Origin: *
  Access-Control-Allow-Credentials: true
  Allow: GET
  Content-Type: text/plain

Response body:

::

    OK

Custom live monitoring event
''''''''''''''''''''''''''''

This check can be defined into the app even subscribers

::

 from django.dispatch import receiver
  from anexia_monitoring.events import monitor_up_check

  @receiver(monitor_up_check)
  def list_of_complete_polls_handler(sender, **kwargs):
      """
      My custom is alive check
      """
      pass


List of developers
------------------

-  Harald Nezbeda, Lead developer

Project related external resources
----------------------------------

-  `Django
   documentation <https://docs.djangoproject.com/en/1.11/>`__
