from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('party.views',
    url(r'sCreate/(?P<eventScheduleId>\d+)$', 'silentCreate'),
)
