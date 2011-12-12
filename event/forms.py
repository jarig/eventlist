from django.db.models.query import QuerySet
from django.forms.formsets import BaseFormSet, formset_factory
from django.forms.models import ModelForm, BaseModelFormSet, modelformset_factory
from django.forms.widgets import HiddenInput
from blogs.models import Blog
from common.forms import AddressForm
from common.models import Address
from common.utils import uploadLocalImage
from event.models import Event, EventSchedule
from django import forms
from organization.models import Organization

class NewEventForm(ModelForm):
    organizers = forms.ModelMultipleChoiceField(Organization.objects.none(),
                                                widget=forms.SelectMultiple(attrs={'placeholder':"Choose an organizers"}))
    logo = forms.CharField(widget=HiddenInput)

    def __init__(self, user, *args, **kwargs):
        super(NewEventForm, self).__init__(*args, **kwargs)
        self.fields['organizers'].queryset = Organization.objects.filter(members=user).all()

    class Meta:
        exclude = ('rating','created','participants','author')
        model = Event
        widgets = {
            'blogId': forms.HiddenInput(),
            'blogs': forms.SelectMultiple(attrs={'placeholder':'Select Event Place'})
        }
        
    def saveEvent(self, request, eventSchedules):
        print "Saving event"
        newEvent = self.save(commit=False)
        newEvent.author = request.user
        newEvent.save()
        
        for schedule in eventSchedules.forms:
            blogId = schedule.cleaned_data["blog"]
            if blogId is not None: newEvent.blogs.add(blogId)
        self.save_m2m() #save manyToMany rls

        eventSchedules.saveSchedules(newEvent)
        
        #save logo
        uploadLocalImage(self.cleaned_data["logo"],
                         str(newEvent.pk) + '_logo',
                         newEvent.logo.save)

        return newEvent


class EventScheduleForm(ModelForm):
    dateFrom = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y',
                                                                                attrs={
                                                                                    "class":"dateFrom"
                                                                                }))
    dateTo = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y',
                                                                                attrs={
                                                                                    "class":"dateTo"
                                                                                }), required=False)
    blog = forms.ModelChoiceField(queryset=Blog.objects.all(),empty_label="Custom Address")
    address = forms.IntegerField(widget=HiddenInput())

    def __init__(self, *args, **kwargs):
        super(EventScheduleForm, self).__init__(*args, **kwargs)
        self.blogId = None
        self.addresses = []

    def saveSchedule(self, event, addressForms):
        schedule = self.save(commit=False)
        schedule.event = event
        if self.blogId is not None:
            #get address id
            schedule.address = Address.objects.get(pk=self.cleaned_data["address"])
        else:
            #create address
            for aForm in addressForms:
                schedule.address = aForm.save()
        schedule.save()
        
        return schedule

    class Meta:
        model = EventSchedule
        widgets = {
            'timeFrom': forms.TimeInput(format='%H:%M'),
            'timeTo': forms.TimeInput(format='%H:%M'),
            'blog': forms.Select(attrs={'placeholder':'Select Event Place'})
        }

class EventScheduleFormSet(BaseModelFormSet):
    
    def __init__(self, *args, **kwargs):
        extra = 0
        if kwargs.has_key("queryset") and not len(kwargs["queryset"]):
            extra = 1
        self.addressSet = modelformset_factory(Address, form=AddressForm, can_delete=True,extra=extra)
        super(EventScheduleFormSet, self).__init__(*args, **kwargs)



    def add_fields(self, form, index):
        super(EventScheduleFormSet, self).add_fields(form, index)
        data = None
        addresses = Address.objects.none()
        if len(self.data):  data = self.data
        try:
            addresses = Address.objects.filter(pk=form.instance.address.pk)
        except Address.DoesNotExist:
            pass

        form.addresses = self.addressSet(prefix='%s-address' % str(form.prefix),
                                         queryset=addresses,
                                         data=data)

    def is_valid(self):
        result = super(EventScheduleFormSet, self).is_valid()

        for form in self.forms:
            try:
                blogId = int(form.data[form.prefix+"-blog"])
                form.blogId = blogId
                continue
            except ValueError as e:
                if not form.addresses.is_valid():
                    return False

        return result
    
    def saveSchedules(self, event):
        print "Saving schedules"
        schedules = []
        for schForm in self.forms:
            schedules.append(schForm.saveSchedule(schForm.addresses.forms))
                
        return schedules