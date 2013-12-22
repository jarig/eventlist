from django.conf.urls import patterns, url

urlpatterns = patterns('party.views',
    url(r'forEvent/(?P<eventScheduleId>\d+)$', 'forEvent'),
    url(r'inviteToEvent/(?P<eventScheduleId>\d+)$', 'inviteToEvent'),
    url(r'manage$', 'manage'),
    url(r'create$', 'create'),
    url(r'edit/(?P<party>\d+)$', 'edit'),


    url(r'invitationList/(?P<eventScheduleId>\d+)$', 'invitationList'),
)
