from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('event.views',
    url(r'create/$', 'create'),
    url(r'edit/(?P<eventId>\d+)$', 'edit'),
    url(r'manage$', 'manage'),
    url(r'^$', 'main'),
)
