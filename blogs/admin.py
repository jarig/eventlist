from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from blogs.models import Types

class BlogTypesAdmin(admin.ModelAdmin):
    pass



admin.site.register(Types, BlogTypesAdmin)
  