from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('organization.views',
    url(r'create/$', 'create'),
    url(r'create/(?P<orgId>\d+)$', 'create'),
)
