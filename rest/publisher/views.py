# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from publisher.forms import RequestForm
from publisher.models import PublisherRequest


@login_required
def index(request):
    request.session["publishMode"] = True
    return HttpResponseRedirect(reverse('blogs.views.manage'))


@login_required
def publisherRequest(request):

    publishRequest = PublisherRequest.objects.filter(user=request.user)
    requestForm = None
    requestMessage = None
    if publishRequest:
        requestMessage = str(publishRequest[0].message)
    else:
        if request.POST:
            requestForm = RequestForm(request.POST)
            if requestForm.is_valid():
                requestForm.save(request)
                messages.success(request, "Your's request successfully send!")
                requestMessage = requestForm.cleaned_data["requestMessage"]
        else:
            requestForm = RequestForm()
    
    return render_to_response('publisher/publisher_request.html',
                              {
                                'requestMessage': requestMessage,
                                'requestForm': requestForm
                              },
                              context_instance=RequestContext(request))




@login_required
@transaction.commit_on_success
def acceptRequest(request, reqIds):
    user = request.user
    #TODO: take referer from next var in REQUEST object
    referer = request.META["HTTP_REFERER"]
    requestIds = reqIds.split(",")
    if user.is_superuser:
        for requestId in requestIds:
            publishPerm = Permission.objects.get(codename="publish")
            publishRequest = PublisherRequest.objects.get(pk=requestId)
            requester = publishRequest.user
            requester.user_permissions.add(publishPerm)
            publishRequest.status = "A" #request status
            publishRequest.save()
            requester.save()
    else:
        messages.error(request, "You don't have permissions")

    successMessage = str(len(requestIds)) + " request successfully accepted"

    messages.success(request, successMessage)
    return HttpResponseRedirect(referer)
    pass



