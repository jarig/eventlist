from django import forms
from django.forms.models import ModelForm
from django.forms.widgets import HiddenInput
from common.fields import ImagePreviewField
from common.models import Address
import event
from party.models import Party

class CreatePartyForm(ModelForm):
    location = forms.ModelChoiceField(queryset=Address.objects.none(),
                                      empty_label="Use Event Address")

    class Meta:
        model = Party

    #def save(self, commit=True):
    #    return self.save()

