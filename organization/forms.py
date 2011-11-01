from django.forms.models import ModelForm
from organization.models import Organization, OrgAccess

class OrganizationForm(ModelForm):


    class Meta:
        exclude = ('address','members')
        model = Organization
    
    def saveOrganization(self, request, address):
        oId = self.instance.pk
        
        organization = self.save(commit=False)
        #fill data
        organization.address = address
        organization.save()

        if oId is None:#if new organization
            oAccess = OrgAccess(member=request.user, organization=organization, level=OrgAccess.OWNER)
            oAccess.save()

        return self.save()