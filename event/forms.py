from django.forms.models import ModelForm
from django.forms.widgets import HiddenInput
from common.utils import uploadLocalImage
from event.models import Event
from django import forms
from organization.models import Organization

class NewEventForm(ModelForm):
    dateFrom = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y'))
    dateTo = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y'))
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
            'dateTo': forms.DateInput(format='%d/%m/%Y'),
            'timeFrom': forms.TimeInput(format='%H:%M'),
            'timeTo': forms.TimeInput(format='%H:%M'),
            'blogs': forms.SelectMultiple(attrs={'placeholder':'Select Event Place'})
        }
        
    def saveEvent(self, request, addresses):
        newEvent = self.save()
        newEvent.author = request.user
        newEvent.addresses = addresses
        
        newEvent.save()
        

        #save logo
        uploadLocalImage(self.cleaned_data["logo"],
                         str(newEvent.pk) + '_logo',
                         newEvent.logo.save)

        return newEvent