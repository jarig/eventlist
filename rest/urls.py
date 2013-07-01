from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^party/', include('party.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^blog_modules/', include('blog_modules.urls')),
    url(r'^accounts/', include('account.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^publisher/', include('publisher.urls')),
    url(r'^common/', include('common.urls')),
    url(r'^event/', include('event.urls')),
    url(r'^organization/', include('organization.urls')),
    url(r'^messaging/', include('messaging.urls')),
    url(r'^ext/pibu/', include('_ext.pibu.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
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
        url(r'^favicon\.ico$',
            RedirectView.as_view(url=settings.MEDIA_URL+'common/favicon.ico')),
   )