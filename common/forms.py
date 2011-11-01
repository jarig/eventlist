from django import forms
from django.forms.models import ModelForm
from common.models import Address, Country, City

class AddressForm(ModelForm):
    country = forms.ModelChoiceField(Country.objects.all(),
                                     empty_label=None)
    city = forms.ModelChoiceField(City.objects.none(),
                                    empty_label='Select City')

    class Meta:
        model = Address
        
    def saveAddress(self, request):
        
        return self.save()