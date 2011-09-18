from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.defaultfilters import title
from django.utils.safestring import mark_safe
import publisher
from publisher.models import PublisherRequest

class PublisherRequestAdmin(admin.ModelAdmin):
    exclude = ('user',)
    actions = ['acceptRequest']
    list_display=('name','message','status','actionButtons')
    list_filter = ('status',)
    pass

    def name(self, obj):
        return mark_safe(obj.user.first_name + " "+ obj.user.last_name)

    def message(self, obj):
        message = obj.message
        #if len(message) > 20:  message = message[:20] + "..."
        return mark_safe(message)

    def status(self, obj):
        return mark_safe(obj.status)

    def actionButtons(self,obj):
        return mark_safe("<a href='"+reverse('publisher.views.acceptRequest', args=[obj.id])+"'>Accept</a> | "+
                         "<a href=''>Reject</a>")
    actionButtons.allow_tags = True
    actionButtons.short_description = "Request Actions"

    def acceptRequest(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect(reverse('publisher.views.acceptRequest', args=[",".join(selected)]))
        pass



admin.site.register(PublisherRequest, PublisherRequestAdmin)
  