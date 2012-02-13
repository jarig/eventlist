from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('party.views',
    url(r'create/(?P<eventScheduleId>\d+)$', 'createWithEvent'),
)
