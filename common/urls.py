from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('common.views',
    url(r'^user$', 'userMode'),
    url(r'^publisher$', 'publisherMode'),
)
