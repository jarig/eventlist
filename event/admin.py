from django.contrib import admin
from event.models import EventActivity

class EventActivityAdmin(admin.ModelAdmin):
    pass



admin.site.register(EventActivity, EventActivityAdmin)