from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('messaging.views',
    url(r'^$', 'messagingReceived'),
    url(r'^sendMessageTo$', 'sendMessageTo'),
    url(r'^sendMessageTo/(?P<user>\d+)$', 'sendMessageTo'),
)
