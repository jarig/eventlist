from django.conf.urls import patterns, url

urlpatterns = patterns('event.views',
    url(r'create$', 'credit'),
    url(r'edit/(?P<event>\d+)$', 'credit'),
    url(r'manage$', 'manage'),
    url(r'go/(?P<eventSchId>\d+)$', 'go'),
    url(r'unGo/(?P<eventSchId>\d+)$', 'unGo'),
    url(r'(?P<scheduleId>\d+)$', 'view_schedule'),
    url(r'^groups$', 'showEventGroups'),
    url(r'^events$', 'showEvents'),
    url(r'^$', 'showEventGroups'),
)