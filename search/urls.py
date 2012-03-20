from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('search.views',
    url(r'^place$', 'findPlace'),
    url(r'^party$', 'findParty'),
    url(r'^people$', 'findPeople'),
)
