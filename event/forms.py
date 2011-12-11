from django.forms.formsets import BaseFormSet, formset_factory
from django.forms.models import ModelForm
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
        newEvent = self.save()
        newEvent.author = request.user
        #TODO save schdules
        
        newEvent.save()
        
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
    
    def __init__(self, *args, **kwargs):
        super(EventScheduleForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = EventSchedule
        widgets = {
            'timeFrom': forms.TimeInput(format='%H:%M'),
            'timeTo': forms.TimeInput(format='%H:%M'),
            'blog': forms.Select(attrs={'placeholder':'Select Event Place'})
        }

class EventScheduleFormSet(BaseFormSet):
    
    def __init__(self, *args, **kwargs):
        self.addressSet = formset_factory(AddressForm, can_delete=True)
        super(EventScheduleFormSet, self).__init__(*args, **kwargs)
        

    def add_fields(self, form, index):
        super(EventScheduleFormSet, self).add_fields(form, index)
        data = None
        if len(self.data):  data = self.data
        form.addresses = self.addressSet(prefix='%s-address' % str(form.prefix),data=data)

    def is_valid(self):
        result = super(EventScheduleFormSet, self).is_valid()

        for form in self.forms:
            blogId = form.data[form.prefix+"-blog"]
            if isinstance(blogId,int) and blogId > 0: break
            if not form.addresses.is_valid():
                return False

        return result