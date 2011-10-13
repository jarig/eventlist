from django.forms.models import ModelForm
from event.models import Event
from django import forms

class NewEventForm(ModelForm):

    class Meta:
        exclude = ('rating','created','participants')
        model = Event
        widgets = {
            'blogId': forms.HiddenInput(),
            'dateFrom': forms.DateTimeInput(format='%d/%m/%Y %H:%M'),
            'dateTo': forms.DateTimeInput(format='%d/%m/%Y %H:%M'),
        }