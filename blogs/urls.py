from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('blogs.views',
    url(r'^manage$', 'manage'),
    url(r'^create$', 'create'),
    url(r'^(?P<blogId>\d+)/edit/(?P<page>\w*)', 'edit'),
    url(r'^(?P<blogId>\d+)/(?P<page>\w*)', 'view'),
    url(r'^getBlogAddress', 'getBlogAddress'),
    url(r'^getAvailableModules','getAvailableModules'),
)
