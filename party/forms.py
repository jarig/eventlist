from django import forms
from django.forms.models import ModelForm
from common.models import Address
from party.models import Party

class CreatePartyForm(ModelForm):
    location = forms.ModelChoiceField(queryset=Address.objects.none(),
                                      empty_label="Use Event Address")

    class Meta:
        model = Party

    #def save(self, commit=True):
    #    return self.save()

