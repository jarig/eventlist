from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('event.views',
    url(r'create/(?P<blogId>\d+)$', 'create'),
    url(r'^$', 'main')
)
