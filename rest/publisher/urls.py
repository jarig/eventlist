from django.conf.urls import patterns, url

urlpatterns = patterns('publisher.views',
    url(r'^request/$', 'publisherRequest'),
    url(r'^request/accept/(?P<reqIds>\d+)/$', 'acceptRequest')
)
