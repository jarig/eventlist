from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('event.views',
    url(r'create/$', 'credit'),
    url(r'edit/(?P<event>\d+)$', 'credit'),
    url(r'manage$', 'manage'),
    url(r'^$', 'main'),
)
