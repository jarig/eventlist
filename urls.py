from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^blog/', include('blogs.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^publisher/', include('publisher.urls')),
    url(r'^common/', include('common.urls')),
    url(r'^event/', include('event.urls')),
    url(r'^organization/', include('organization.urls')),
    url(r'^$', 'common.views.index'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )