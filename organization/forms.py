import os
from django import forms
from django.core.files.images import get_image_dimensions
from django.forms.models import ModelForm
from django.utils.translation import ugettext
from common.utils import uploadLocalImage, urlToPath
from common.widgets import HiddenImageInput
from organization.models import Organization, OrgAccess

class OrganizationForm(ModelForm):
    logo = forms.CharField(widget=HiddenImageInput)

    class Meta:
        exclude = ('address','members')
        model = Organization

    def clean_logo(self):
       logoURL = self.cleaned_data.get("logo")
       if not logoURL:
           raise forms.ValidationError("No image!")
       else:
           logoPath= urlToPath(logoURL)
           if not os.path.exists(logoPath):
               raise forms.ValidationError(ugettext("Image doesn't exist"))
           w, h = get_image_dimensions(logoPath)
           if w > 256:
               raise forms.ValidationError("The image is %i pixel wide. It's supposed to be 256px" % w)
           if h > 256:
               raise forms.ValidationError("The image is %i pixel high. It's supposed to be 256px" % h)
       return logoURL
    
    def saveOrganization(self, request, address):
        oId = self.instance.pk
        
        organization = self.save(commit=False)
        organization.address = address
        organization.save()
        #save logo
        uploadLocalImage(self.cleaned_data["logo"],
                         str(organization.pk)+'_logo',
                         organization.logo.save)
        

        if oId is None:#if new organization
            oAccess = OrgAccess(member=request.user, organization=organization, level=OrgAccess.OWNER)
            oAccess.save()
        
        return self.save()