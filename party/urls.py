from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('party.views',
    url(r'forEvent/(?P<eventScheduleId>\d+)$', 'forEvent'),
    url(r'inviteToEvent/(?P<eventScheduleId>\d+)$', 'inviteToEvent'),
    url(r'manage$', 'manage'),
    url(r'create$', 'credit'),


    url(r'getInvitationList/(?P<eventScheduleId>\d+)$', 'getInvitationList'),
)
