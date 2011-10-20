from django.conf.urls.defaults import *

urlpatterns = patterns(
    'smarterer_auth.views',
    url(r'^authorize/$', 'authorize', name='smarterer_auth-authorize'),
    url(r'^callback/$', 'callback', name='smarterer_auth-callback'),
    )
