from django.conf.urls import patterns, url

urlpatterns = patterns('account.views',
    # Examples:
    url(r'^$', 'profile'),
    url(r'^edit$', 'edit'),
    url(r'^elogin', 'extLoginProfile'),
    url(r'^logout$', 'logoutProfile'),
    url(r'^login$', 'nativeLogin'),
    url(r'^friends$', 'friendlist'),
    url(r'^getFriends$', 'getFriends'),
    url(r'^addFriend/(?P<user>\d+)$', 'addFriend'),
    url(r'^register$', 'register'),
)
