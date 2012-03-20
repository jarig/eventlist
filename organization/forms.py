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

    class Meta:
        exclude = ('address','members')
        model = Organization

    
    def saveOrganization(self, request, address):
        oId = self.instance.pk
        
        organization = self.save(commit=False)
        organization.address = address
        organization.save()

        if oId is None:#if new organization
            oAccess = OrgAccess(member=request.user, organization=organization, level=OrgAccess.OWNER)
            oAccess.save()
        
        return self.save()