# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from common.forms import AddressForm
from common.models import City, Country
from organization.forms import OrganizationForm
from organization.models import Organization


@login_required
@permission_required('publisher.publish')
def create(request, orgId=None):
    address = None
    organization = None
    if orgId is None: orgId = request.REQUEST.get('orgId',None)
    if orgId is not None:
        organization = Organization.objects.get(pk=orgId)
        address = organization.address
    postData = request.POST
    if not len(postData): postData=None
    adrData = postData
    
    if adrData is None and address is None:
        adrData = {'country': Country.objects.get(name='Estonia')}

    adrForm = AddressForm(adrData,
                          instance=address)

    countryVal = adrForm.initial.get('country',None)
    if adrForm.data.has_key("country"):
        countryVal = adrForm.data.get('country',0)

    cities = City.objects.filter(country=countryVal).all()
    adrForm.fields['city'].queryset = cities

    if request.POST:
        #adrForm = AddressForm(request.POST, instance=address)
        orgForm = OrganizationForm(request.POST, request.FILES, instance=organization)
        if orgForm.is_valid() and adrForm.is_valid():
            address = adrForm.save()
            organization = orgForm.saveOrganization(request, address)
            messages.success(request, "Organization successfully created")
            HttpResponseRedirect(reverse('organization.views.create',kwargs={'orgId':organization.pk}))#redirect to edit
        pass
    else:
        orgForm = OrganizationForm(instance=organization)
    

        
    return render_to_response("organization/organization_page.html",
                              {
                                "orgForm": orgForm,
                                "adrForm": adrForm,
                              },
                              context_instance=RequestContext(request)
                              )