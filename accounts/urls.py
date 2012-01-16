from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('accounts.views',
    # Examples:
    url(r'^$', 'profile'),
    url(r'^edit$', 'edit'),
    url(r'^elogin', 'extLoginProfile'),
    url(r'^logout$', 'logoutProfile'),
    url(r'^login/$', 'nativeLogin'),
    url(r'^friends$', 'friendlist'),
    url(r'^messages', 'messages'),
)
