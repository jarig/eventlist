from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from blog.models import FacilityType

class FacilityTypeAdmin(admin.ModelAdmin):
    pass



admin.site.register(FacilityType, FacilityTypeAdmin)
  