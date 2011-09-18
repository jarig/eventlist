from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('rest.views',
    url(r'^find/place$', 'findPlace'),
    url(r'^find/$', 'findPlace'),
    url(r'^find/party$', 'findParty')
)
