from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('party.views',
    url(r'forEvent/(?P<eventScheduleId>\d+)$', 'forEvent'),
    url(r'inviteToEvent/(?P<eventScheduleId>\d+)$', 'inviteToEvent'),
    url(r'manage$', 'manage'),
    url(r'create$', 'create'),
    url(r'edit/(?P<partyId>\d+)$', 'edit'),


    url(r'invitationList/(?P<eventScheduleId>\d+)$', 'invitationList'),
)
