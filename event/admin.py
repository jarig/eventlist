from django.contrib import admin
from django import forms
from event.models import EventActivity, EventGroup


class EventActivityAdmin(admin.ModelAdmin):
    pass


admin.site.register(EventActivity, EventActivityAdmin)


class EventActivityInline(admin.TabularInline):
    model = EventActivity


class EventGroupAdminForm(forms.ModelForm):
    activities = forms.ModelMultipleChoiceField(EventActivity.objects.all())

    def __init__(self, *args, **kwargs):
        super(EventGroupAdminForm, self).__init__(*args, **kwargs)
        assignedActivities = EventActivity.objects.filter(group=self.instance).values_list('pk', flat=True)
        initialActivities = dict()
        for act in assignedActivities:
            initialActivities[act] = True
        self.fields['activities'].initial = initialActivities

    def save(self, commit=True):
        inst = super(EventGroupAdminForm, self).save(commit=False)
        inst.activities = self.cleaned_data["activities"]
        inst.save()
        return inst

    class Meta:
        model = EventGroup


class EventGroupAdmin(admin.ModelAdmin):
    form = EventGroupAdminForm
    pass

admin.site.register(EventGroup, EventGroupAdmin)