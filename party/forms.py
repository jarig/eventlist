from django import forms
from django.forms.models import ModelForm
from party.models import Party

class CreateSimplePartyForm(ModelForm):

    class Meta:
        model = Party
        widgets = {
            'author': forms.HiddenInput
        }
