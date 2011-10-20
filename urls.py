from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns(
    '',
    url(r'^_ah/warmup$', 'djangoappengine.views.warmup'),
    url('^$', 'django.views.generic.simple.direct_to_template',
        {'template': 'home.html'}),
    url('^smarterer_auth/', include('smarterer_auth.urls')),
)
