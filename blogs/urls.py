from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('blogs.views',
    url(r'^manage$', 'manage'),
    url(r'^create$', 'create'),
    url(r'^edit/(?P<blogId>\d+)', 'edit'),
    url(r'^uploadTempImage$', 'uploadTempImage'),
)
