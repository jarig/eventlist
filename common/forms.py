from django import forms
from django.forms.models import ModelForm
from common.models import Address, Country, City

class AddressForm(ModelForm):
    country = forms.ModelChoiceField(Country.objects.all(),
                                     cache_choices=True,
                                     empty_label=None,
                                     widget=forms.Select(attrs={'placeholder':'Select Country'}))
    city = forms.ModelChoiceField(City.objects.none(),
                                    cache_choices=True,
                                    empty_label=None,
                                    widget=forms.Select(attrs={'placeholder':'Select City'}))
    
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        countryVal = self.__getitem__('country').value()
        if countryVal is None: countryVal = 1
        self.fields['city'].queryset = City.objects.filter(country=countryVal).all()

    class Meta:
        model = Address
        widgets = {
            'street': forms.TextInput(attrs={'title':'Street'}),
            'county': forms.TextInput(attrs={'title':'County'}),
            'cityArea': forms.TextInput(attrs={'title':'City Area'}),
            'postalCode': forms.TextInput(attrs={'title':'Postal Code'}),
        }
    
#    def save(self, commit=True):
#        super(AddressForm, self).save(commit)
        

    def saveAddress(self, request):
        
        return self.save()