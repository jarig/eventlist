from django.forms.models import ModelForm
from event.models import Event
from django import forms
from organization.models import Organization

class NewEventForm(ModelForm):
    dateFrom = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y'))
    dateTo = forms.DateField(input_formats=['%d/%m/%Y'])
    organizers = forms.ModelMultipleChoiceField(Organization.objects.none(),
                                                widget=forms.SelectMultiple(attrs={'placeholder':"Choose an organizers"}))

    def __init__(self, user, *args, **kwargs):
        super(NewEventForm, self).__init__(*args, **kwargs)
        self.fields['organizers'].queryset = Organization.objects.filter(members=user)

    class Meta:
        exclude = ('rating','created','participants','author')
        model = Event
        widgets = {
            'blogId': forms.HiddenInput(),
            'dateTo': forms.DateInput(format='%d/%m/%Y'),
            'timeFrom': forms.TimeInput(format='%H:%M'),
            'timeTo': forms.TimeInput(format='%H:%M')
        }
        
    def saveEvent(self, request):
        newEvent = self.save(commit=False)
        newEvent.author = request.user
        

        return self.save()