from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^blog/', include('blogs.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^rest/', include('rest.urls')),
    url(r'^publisher/', include('publisher.urls')),
    url(r'^', include('events.urls')),
    # url(r'^publish/', include('publish.urls')),
    # url(r'^eventlist/', include('eventlist.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
