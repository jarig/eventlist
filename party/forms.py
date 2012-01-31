from django import forms
from django.forms.models import ModelForm
import event
from party.models import Party

class CreateSimplePartyForm(ModelForm):

    class Meta:
        model = Party
        widgets = {
            'author': forms.HiddenInput
        }

    #def save(self, commit=True):
    #    return self.save()

