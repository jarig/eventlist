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
def credit(request, orgId=None):
    address = None
    organization = None
    if orgId is not None:
        organization = Organization.objects.get(pk=orgId)
        address = organization.address

    if request.POST:
        #adrForm = AddressForm(request.POST, instance=address)
        orgForm = OrganizationForm(request.POST, request.FILES, instance=organization)
        adrForm = AddressForm(request.POST, instance=address)
        if orgForm.is_valid() and adrForm.is_valid():
            address = adrForm.save()
            organization = orgForm.saveOrganization(request, address)
            messages.success(request, "Organization successfully saved")
            HttpResponseRedirect(reverse('organization.views.credit',kwargs={'orgId':organization.pk}))#redirect to edit
        pass
    else:
        orgForm = OrganizationForm(instance=organization)
        adrForm = AddressForm(instance=address,
                              initial={'country':Country.objects.get(name='Estonia').pk})
    

        
    return render_to_response("organization/organization_page.html",
                              {
                                "orgForm": orgForm,
                                "adrForm": adrForm,
                              },
                              context_instance=RequestContext(request)
                              )

@login_required
def manage(request):
    myOrgs = Organization.objects.filter(members=request.user)
    return render_to_response("organization/organization_manage.html",
                              {
                                "myOrgs": myOrgs,
                              },
                              context_instance=RequestContext(request)
                              )
    pass