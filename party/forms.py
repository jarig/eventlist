from django import forms
from django.forms.models import ModelForm, BaseModelFormSet
from _ext.autocomplete import fields
from account.models import Account
from common.models import Address
from party.models import Party, PartySchedule, PartyMember

class CreatePartyForm(ModelForm):
    #invited = forms.MultiValueField()

    class Meta:
        model = Party

    def saveParty(self, author, schedulesFormSet, invited):

        party = self.save(commit=False)
        party.author = author
        party.save()
        #save invited members
        authorMember = PartyMember(party=party, user=author, role=PartyMember.ROLE.OWNER, invitedBy=None)
        authorMember.save()
        for inv in invited:
            if inv == "": continue
            pm = PartyMember(party=party, user=Account(pk=inv), role=PartyMember.ROLE.INVITED, invitedBy=author)
            #TODO bulk save
            pm.save()

        schedules  = schedulesFormSet.save(commit=False)
        for schedule in schedules:
            schedule.party = party
            schedule.save()
        return party

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
        return self.cleaned_data['location']

    class Meta:
        model = PartySchedule
        widgets = {
            'timeFrom': forms.TimeInput(format='%H:%M', attrs={'placeholder':'Time From'}),
            'timeTo': forms.TimeInput(format='%H:%M', attrs={'placeholder':'Time To'})
        }
        exclude = ('eventSchedule', 'url')


