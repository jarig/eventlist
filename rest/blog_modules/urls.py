from django.conf.urls import patterns, url

urlpatterns = patterns('blog_modules.views',
    url(r'^list/(?P<style>\w+)/(?P<position>\d+)$', 'getModuleList'),
    url(r'^render$', 'renderModule'),
)
