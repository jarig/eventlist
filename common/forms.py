from django import forms
from django.core.files.storage import DefaultStorage
from django.forms.fields import ImageField
from django.forms.forms import Form
from django.forms.models import ModelForm
from common.models import Address, Country, City
from common.widgets import PreviewImageInput

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


class TempImageForm(Form):
    image = ImageField()


class ImagePreviewField(ImageField):
    widget = PreviewImageInput # Default widget to use when rendering this type of Field.

    def to_python(self, data):
        storage = DefaultStorage()
        print "To python: " + str(data)
        return  super(ImagePreviewField, self).to_python(storage.open(data))

    def clean(self, data, initial=None):
        storage = DefaultStorage()

        print "Clean: "+str(data)
        print "Initial: "+str(initial)
        return super(ImagePreviewField, self).clean(storage.open(data), initial)

    def bound_data(self, data, initial):
        print "Bounded data:" + str(data)
        return super(ImagePreviewField, self).bound_data(data, initial)