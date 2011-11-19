import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext
from blogs.models import Blog
from common.models import Address
from event.forms import NewEventForm
from event.models import Event


def render_event(request, attrs):

    return render_to_response("events/events_event.html",
                                  attrs,
                                  context_instance=RequestContext(request)
                                  )

@login_required
@permission_required('publisher.publish')
def create(request, blogId=None):
    blog = None
    addresses = []
    if blogId is not None:
        blog = Blog.objects.get(pk=blogId)
        addresses = blog.addresses.all()
    

    if request.method == "POST":
        #get addresses
        if request.POST.has_key(u"adr_id"):
            addressIds = request.POST.getlist('adr_id')
            for id in addressIds:
                if id == '': continue
                addresses.append(Address.objects.get(pk=id))
        eventForm = NewEventForm(request.user, request.POST, request.FILES)
        if eventForm.is_valid():
            newEvent = eventForm.saveEvent(request)
            messages.success(request, ugettext("Event successfully created"))
            #redirect to edit/publish event
            return HttpResponseRedirect(reverse("event.views.edit", kwargs={"eventId": newEvent.id}))
    else:
        eventForm = NewEventForm(request.user,
                                 initial={'dateFrom':datetime.date.today(),
                                          'timeFrom':'00:00',
                                          'timeTo':'00:00'
        })
    

    return render_event(request, {
                                    "blog": blog,
                                    "addresses": addresses,
                                    "eventForm": eventForm,
                                 })
    pass

@login_required
@permission_required('publisher.publish')
def edit(request, eventId):
    event = Event.objects.select_related('blogs').get(pk=eventId)
    if event.author != request.user:
        raise Event.DoesNotExist(_("You don't have permission to edit this event"))
    if request.method == "POST":
        eventForm = NewEventForm(request.user, request.POST, request.FILES, instance=event)
        if eventForm.is_valid():
            eventForm.saveEvent(request)
            messages.success(request, ugettext("Event details successfully changed."))
    else:
        eventForm = NewEventForm(request.user, instance=event)
        
    addresses = event.addresses.all()
    return render_event(request,{
                                    "eventForm":eventForm,
                                    "addresses":addresses
                                })



def main(request):
    return render_to_response("events/events_main.html",
                              {
                              },
                              context_instance=RequestContext(request)
                              )

