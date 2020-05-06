Anexia Monitoring
=================

A Django app used to monitor updates for Django and all installed python
packages in the running environment. It can be also used to check if the
website is alive and working correctly.

Installation and configuration
------------------------------

Install the package by using pip

```bash
pip install django-anexia-monitoring
```

Add the app the settings installed apps

```python
INSTALLED_APPS = [
  ...
  # Anexia monitor
  'anexia_monitoring',
  ...
]
```

In the projects settings.py add the access token configuration:

```python
ANX_MONITORING_ACCESS_TOKEN = 'custom_access_token'
```

Add URL configuration for REST endpoint

```python
from anexia_monitoring import urls as monitor_urls
...
urlpatterns = [
  ...
  # Anexia monitoring
  url(r'^', include(monitor_urls)),
  ...
]
```

Usage
-----

The plugin registers some custom REST endpoints which can be used for
monitoring. Make sure that the **ANX\_MONITORING\_ACCESS\_TOKEN** is
defined, since this is used for authorization. The endpoints will return
a 401 HTTP\_STATUS code if the token is not define or invalid, and a 200
status code otherwise.

### Version monitoring

Returns all a list with platform and module information.

**URL:** `/anxapi/v1/modules/?access_token=custom_access_token`

Response headers:

```text
Status Code: 200 OK
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Allow: GET
Content-Type: application/json
```

Response body:

```json
{
   "platform":{
      "platform":"python",
      "framework_installed_version":"1.11.1",
      "framework_newest_version":"2.0a1",
      "framework":"django",
      "platform_version":"3.5.3 (default, Apr 26 2017, 20:12:19) \n[GCC 4.9.2]"
   },
   "modules":[
      {
         "newest_version":"1.4.3",
         "newest_version_licences": [
           "MIT"
         ],
         "name":"appdirs",
         "installed_version":"1.4.3",
         "installed_version_licences": [
           "MIT"
         ]
      },
      {
         "newest_version":"0.22.0",
         "newest_version_licences": [
           "MIT"
         ],
         "name":"asn1crypto",
         "installed_version":"0.22.0",
         "installed_version_licences": [
           "MIT"
         ],
      },
      {
         "newest_version":"2.4.0",
         "newest_version_licences": [
           "BSD"
         ],
         "name":"Babel",
         "installed_version":"2.4.0",
         "installed_version_licences": [
           "BSD"
         ],
      }
   ]
}
```

### Live monitoring

This endpoint can be used to verify if the application is alive and
working correctly. It checks if the database connection is working and
makes a query for users. It allows to register custom checks by using
the dispatched **monitor\_up\_check** event.

**URL:** `/anxapi/v1/up/?access_token=custom_access_token`

Response headers:

```text
Status Code: 200 OK
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Allow: GET
Content-Type: text/plain
```

Response body:

```text
OK
```

#### Custom live monitoring event

This check can be defined into the app even subscribers

```python
from django.dispatch import receiver
from anexia_monitoring.events import monitor_up_check

@receiver(monitor_up_check)
def list_of_complete_polls_handler(sender, **kwargs):
    """
    My custom is alive check
    """
    pass
```

#### Live monitoring settings

The User table is used in most Django applications and by default the `up` endpoint will make a test query to this
table. If you don't need it you can disable it using the `ANX_MONITORING_TEST_QUERY_USERS` setting.

Similar most Django applications also use a database connection which the module tests for connection by default.
If you don't need this you can deactivate it by providing the `ANX_MONITORING_TEST_DB_CONNECTIONS` setting.

```python
ANX_MONITORING_TEST_QUERY_USERS = False
ANX_MONITORING_TEST_DB_CONNECTIONS = False
```

List of developers
------------------

-   Harald Nezbeda, Lead developer

Project related external resources
----------------------------------

-   [Django documentation](https://docs.djangoproject.com/en/2.2/)
