from django import forms
from django.forms.models import ModelForm
from common.models import Address
from event.models import EventSchedule
from party.models import Party, PartySchedule

class CreatePartyForm(ModelForm):


    class Meta:
        model = Party

    #def save(self, commit=True):
    #    return self.save()

class PartyScheduleForm(ModelForm):

    eventSchedule = forms.ModelChoiceField(EventSchedule.objects.none(),
        empty_label='Find Event', widget=forms.HiddenInput)
    location = forms.ModelChoiceField(Address.objects.none(), empty_label='Find Place')
    dateFrom = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y',attrs={
        'placeholder': 'Date From',
    }))
    dateTo = forms.DateField(input_formats=['%d/%m/%Y'], required=False,
        widget=forms.DateInput(format='%d/%m/%Y', attrs={
        'placeholder': 'Date To',
    }))

    class Meta:
        model = PartySchedule
        widgets = {
            'timeFrom': forms.TimeInput(format='%H:%M', attrs={'placeholder':'Time From'}),
            'timeTo': forms.TimeInput(format='%H:%M', attrs={'placeholder':'Time To'}),
            'url': forms.TextInput(attrs={'placeholder':'URL'})
        }
