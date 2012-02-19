from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('organization.views',
    url(r'edit/(?P<orgId>\d+)$', 'credit'),
    url(r'create$', 'credit'),
    url(r'manage$', 'manage'),
)
