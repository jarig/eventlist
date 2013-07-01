from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from publisher.models import PublisherRequest

class PublisherRequestAdmin(admin.ModelAdmin):
    exclude = ('user',)
    actions = ['acceptRequest']
    list_display=('name','message','rStatus','actionButtons')
    list_filter = ('status',)
    pass

    def name(self, obj):
        return mark_safe(obj.user.first_name + " "+ obj.user.last_name)

    def message(self, obj):
        message = obj.message
        #if len(message) > 20:  message = message[:20] + "..."
        return mark_safe(message)

    def rStatus(self, obj):
        scaffold = "<ul class='messagelist'><li class='%s'>%s</li></ul>"
        if obj.status == PublisherRequest.STATUS.ACCEPTED:
            return mark_safe(scaffold % ('success',obj.status))
        elif obj.status == PublisherRequest.STATUS.DECLINED:
            return mark_safe(scaffold % ('fail',obj.status))
        else:
            return mark_safe(scaffold % ('warning',obj.status))

    rStatus.allow_tags = True
    rStatus.short_description = "Request Status"

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
  