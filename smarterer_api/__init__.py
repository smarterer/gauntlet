"""
Simple Python wrapper for the Smarterer API.
"""

from google.appengine.api.urlfetch import fetch
from django.utils import simplejson
import urllib

API_BASE_URL = "https://smarterer.com/api/"


class SmartererApiHttpException(Exception):
    pass


class Smarterer(object):
    def __init__(self, access_token=None):
        self.access_token = access_token

    def _fetch(self, url):
        """
        Fetch a URL. If anything other than a 200 OK response is received,
        raise an exception. Otherwise, return the content.
        """
        response = fetch(url, validate_certificate=False)
        if response.status_code != 200:
            raise SmartererApiHttpException("Not-OK response. HTTP Status=%s, "
                                            "Response=%r" % (
                                                response.status_code,
                                                response.content))
        # otherwise, return the content
        return response.content

    def _req(self, resource_name):
        """
        Make an API request over HTTP and attempt to parse the JSON result.

        :param resource_name: Path to the API resource under the main
                              API_BASE_URL.
        """
        url = API_BASE_URL + resource_name
        if self.access_token:
            url += "?" + urllib.urlencode(dict(access_token=self.access_token))

        return simplejson.loads(self._fetch(url))

    def badges(self, username=None):
        resource = "badges"
        if username:
            resource = "/".join((resource, username))
        return self._req(resource)
