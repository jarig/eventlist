from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('organization.views',
    url(r'create/(?P<orgId>\d+)$', 'create'),
    url(r'create/$', 'create'),
)
