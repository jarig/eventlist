from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('publisher.views',
    url(r'^$', 'index'),
    url(r'^request/$', 'publisherRequest'),
    url(r'^request/accept/(?P<reqIds>\d+)/$', 'acceptRequest')
)
