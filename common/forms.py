from django import forms
from django.forms.fields import ImageField
from django.forms.forms import Form
from django.forms.models import ModelForm
from common.models import Address, Country, City

class AddressForm(ModelForm):
    country = forms.ModelChoiceField(Country.objects.all(),
                                     empty_label=None,
                                     widget=forms.Select(attrs={'placeholder':'Select Country'}))
    city = forms.ModelChoiceField(City.objects.none(),
                                    empty_label=None,
                                    widget=forms.Select(attrs={'placeholder':'Select City'}))

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        countryVal = self.__getitem__('country').value()
        
        self.fields['city'].queryset = City.objects.filter(country=countryVal).all()

    class Meta:
        model = Address
        widgets = {
            'street': forms.TextInput(attrs={'title':'Street'}),
            'county': forms.TextInput(attrs={'title':'County'}),
            'cityArea': forms.TextInput(attrs={'title':'City Area'}),
            'postalCode': forms.TextInput(attrs={'title':'Postal Code'}),
        }
        
    def saveAddress(self, request):
        
        return self.save()


class TempImageForm(Form):
    image = ImageField()