from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils import simplejson

import urllib
from google.appengine.api.urlfetch import fetch


def authorize(request):
    # https://smarterer.com/oauth/authorize
    #   ?client_id=abc123...
    #   &callback_url=YOUR_CALLBACK_URL_HERE

    callback_url = request.build_absolute_uri(
        reverse("smarterer_auth-callback"))

    auth_url = "%s?%s" % (settings.SMARTERER_OAUTH_URL_AUTHORIZE,
                          urllib.urlencode(dict(
                              client_id=settings.SMARTERER_CLIENT_ID,
                              callback_url=callback_url,
                              )))
    return HttpResponseRedirect(auth_url)


def _authorization_error(request, message):
    return HttpResponse("Authorization error: %s" % message)


def callback(request):
    code = request.REQUEST.get("code")
    if not code:
        return _authorization_error("Access code missing in redirect.")

    # https://smarterer.com/oauth/access_token
    #   ?client_id=abc123...
    #   &client_secret=abc123...
    #   &grant_type=authorization_code
    #   &code=CODE_FROM_ABOVE

    access_token_url = "%s?%s" % (
        settings.SMARTERER_OAUTH_URL_ACCESS_TOKEN,
        urllib.urlencode(dict(
            client_id=settings.SMARTERER_CLIENT_ID,
            client_secret=settings.SMARTERER_CLIENT_SECRET,
            grant_type="authorization_code",
            code=code,
            )))

    # Note: we're using the AppEngine fetch function here, because it allows
    # us to pass validate_certificate=False in order to skip strict SSL
    # validation. Outside of AppEngine, consider using a different fetch
    # function and enabling SSL validation.
    access_token_info = fetch(access_token_url, validate_certificate=False)

    if access_token_info.status_code != 200:
        return _authorization_error(request, access_token_info.content)

    content = str(access_token_info.content)
    try:
        response_dict = simplejson.loads(content)
    except Exception, e:
        return _authorization_error(request,
                                    "Could not parse access token response "
                                    "from OAuth provider: "
                                    "%s.\nResponse: %r" % (e, content))

    if "access_token" not in response_dict:
        return _authorization_error(request,
                                    "Missing access token in response "
                                    "from OAuth provider. Response was: %r" % (
                                        response_dict))

    return HttpResponse("OK! " + repr(response_dict))
