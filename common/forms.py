from django import forms
from django.forms.fields import ImageField
from django.forms.forms import Form
from django.forms.models import ModelForm
from common.models import Address, Country, City

class AddressForm(ModelForm):
    country = forms.ModelChoiceField(Country.objects.all(),
                                     empty_label=None)
    city = forms.ModelChoiceField(City.objects.none(),
                                    empty_label='Select City')

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        countryVal = 0
        if self.data and self.data.has_key('country'):
            countryVal = self.data['country']
        elif self.initial and self.initial.has_key('country'):
            countryVal=self.initial['country']
        
        self.fields['city'].queryset = City.objects.filter(country=countryVal).all()

    class Meta:
        model = Address
        
    def saveAddress(self, request):
        
        return self.save()


class TempImageForm(Form):
    image = ImageField()