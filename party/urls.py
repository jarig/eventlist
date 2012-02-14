from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('party.views',
    url(r'forEvent/(?P<eventScheduleId>\d+)$', 'forEvent'),
)
