from django.forms.models import ModelForm
from event.models import Event
from django import forms

class NewEventForm(ModelForm):
    dateFrom = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y'))
    dateTo = forms.DateField(input_formats=['%d/%m/%Y'])
    
    class Meta:
        exclude = ('rating','created','participants','author')
        model = Event
        widgets = {
            'blogId': forms.HiddenInput(),
            'dateTo': forms.DateInput(format='%d/%m/%Y'),
            'timeFrom': forms.TimeInput(format='%H:%M'),
            'timeTo': forms.TimeInput(format='%H:%M'),
        }
    def saveEvent(self, request):
        newEvent = self.save(commit=False)
        newEvent.author = request.user
        
        return self.save()