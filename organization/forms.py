import os
from django import forms
from django.core.files.images import get_image_dimensions
from django.core.files.storage import get_storage_class, DefaultStorage
from django.forms.models import ModelForm
from django.forms.widgets import HiddenInput
from django.utils.translation import ugettext
from common.utils import uploadLocalImage
from organization.models import Organization, OrgAccess

class OrganizationForm(ModelForm):
    logo = forms.CharField(widget=HiddenInput)

    class Meta:
        exclude = ('address','members')
        model = Organization

    def clean_logo(self):
       logoPath = self.cleaned_data.get("logo")
       storage = DefaultStorage()
       if not logoPath:
           raise forms.ValidationError("No image!")
       else:
           if not storage.exists(logoPath):
               raise forms.ValidationError(ugettext("Image doesn't exist"))
           w, h = get_image_dimensions(storage.open(logoPath))
           if w > 256:
               raise forms.ValidationError("The image is %i pixel wide. It's supposed to be 256px" % w)
           if h > 256:
               raise forms.ValidationError("The image is %i pixel high. It's supposed to be 256px" % h)
       return logoPath
    
    def saveOrganization(self, request, address):
        oId = self.instance.pk
        
        organization = self.save(commit=False)
        organization.address = address
        organization.save()
        #save logo
        uploadLocalImage(self.cleaned_data["logo"],
                         str(organization.pk) + '_logo',
                         organization.logo.save)
        

        if oId is None:#if new organization
            oAccess = OrgAccess(member=request.user, organization=organization, level=OrgAccess.OWNER)
            oAccess.save()
        
        return self.save()