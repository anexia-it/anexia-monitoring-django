from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings

client = Client()


class MonitoringAPITests(TestCase):
    """
    Test for monitoring endpoints. The endpoints are configured in the main urls.py and come
    from the anexia_monitoring package. The access token must be defined in the django settings.
    """
    def test_monitoring_endpoint(self):
        """
        Ensure the monitoring endpoint can be called
        """
        url = reverse('anexia_monitor_modules')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, 401)

        response = client.get("%s?access_token=invalid_access_token" % url, format='json')
        self.assertEqual(response.status_code, 401)

        response = client.get("%s?access_token=%s" % (url, settings.ANX_MONITORING_ACCESS_TOKEN), format='json')
        self.assertEqual(response.status_code, 200)

    def test_up_endpoint(self):
        """
        Ensure the up endpoint can be called
        """
        url = reverse('anexia_monitor_up')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, 401)

        response = client.get("%s?access_token=invalid_access_token" % url, format='json')
        self.assertEqual(response.status_code, 401)

        response = client.get("%s?access_token=%s" % (url, settings.ANX_MONITORING_ACCESS_TOKEN), format='json')
        self.assertEqual(response.status_code, 200)
