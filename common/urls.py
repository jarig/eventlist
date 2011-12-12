from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('common.views',
    url(r'^index$', 'index'),
    url(r'^user$', 'userMode'),
    url(r'^publisher$', 'publisherMode'),
    url(r'^uploadTempImage$', 'uploadTempImage'),
    url(r'^getCities$', 'getCities'),
    url(r'^getAddress$', 'getAddress'),
)
