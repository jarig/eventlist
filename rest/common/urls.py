from django.conf.urls import patterns, url

urlpatterns = patterns('common.views',
    url(r'^index$', 'index'),
    url(r'^user$', 'userMode'),
    url(r'^publisher$', 'publisherMode'),
    url(r'^getCities$', 'getCities'),
    url(r'^getAddress$', 'getAddress'),
    url(r'^findAddress', 'findAddress'),
)
