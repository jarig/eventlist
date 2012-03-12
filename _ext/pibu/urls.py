from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('_ext.pibu.views',
    url(r'^uploadTempImage$', 'uploadTempImage'),
)
