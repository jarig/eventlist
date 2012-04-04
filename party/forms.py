from django import forms
from django.forms.models import ModelForm, BaseModelFormSet
from _ext.autocomplete import fields
from common.models import Address
from party.models import Party, PartySchedule

class CreatePartyForm(ModelForm):


    class Meta:
        model = Party

    #def save(self, commit=True):
    #    return self.save()

class PartyScheduleFormSet(BaseModelFormSet):
    pass

class EventPartyScheduleForm(ModelForm):
    eventSchedule = forms.CharField(widget=forms.HiddenInput)
    dateFrom = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.HiddenInput)

    class Meta:
        model = PartySchedule
        widgets = {
            'timeFrom': forms.HiddenInput()
        }
        exclude = ('url','dateTo','timeTo', 'location')

class CustomPartyScheduleForm(ModelForm):
    eventSchedule = forms.CharField(widget=forms.HiddenInput, required=False)
    #location = forms.CharField(widget=forms.HiddenInput)
    location = fields.AutoCompleteCharField(model=Address)
    dateFrom = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y',attrs={
        'placeholder': 'Date From',
    }))
    dateTo = forms.DateField(input_formats=['%d/%m/%Y'], required=False,
        widget=forms.DateInput(format='%d/%m/%Y', attrs={
        'placeholder': 'Date To',
    }))

    def clean_location(self):
        return Address(pk=self.cleaned_data['location'])

    class Meta:
        model = PartySchedule
        widgets = {
            'timeFrom': forms.TimeInput(format='%H:%M', attrs={'placeholder':'Time From'}),
            'timeTo': forms.TimeInput(format='%H:%M', attrs={'placeholder':'Time To'})
        }
        exclude = ('eventSchedule', 'url')


