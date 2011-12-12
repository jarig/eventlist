import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.forms.models import  modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext
from event.forms import NewEventForm, EventScheduleForm, EventScheduleFormSet
from event.models import Event, EventSchedule


def render_event(request, attrs):

    return render_to_response("events/events_event.html",
                                  attrs,
                                  context_instance=RequestContext(request)
                                  )

@login_required
@permission_required('publisher.publish')
def credit(request, event=None):
    schedules = EventSchedule.objects.none()
    extraSchedule = 1
    if event is not None:
        event = Event.objects.select_related('blogs').get(pk=event)
        if event.author != request.user:#TODO check organization group
            raise Event.DoesNotExist(_("You don't have permission to edit this event"))
        schedules = EventSchedule.objects.filter(event=event)
        extraSchedule = 0
    
    eventScheduleFormSet = modelformset_factory(EventSchedule,
                                                form=EventScheduleForm,
                                                formset=EventScheduleFormSet, can_delete=True, extra=extraSchedule)
    if request.method == "POST":
        eventForm = NewEventForm(request.user, request.POST, request.FILES,instance=event)
        eventSchedules = eventScheduleFormSet(request.POST,
                                              queryset=schedules)
        if eventForm.is_valid() and eventSchedules.is_valid():
            newEvent = eventForm.saveEvent(request, eventSchedules)
            messages.success(request, ugettext("Event successfully created"))
            #redirect to edit/publish event
            return HttpResponseRedirect(reverse("event.views.edit", kwargs={"eventId": newEvent.id}))
    else:
        eventForm = NewEventForm(request.user, instance=event)
        eventSchedules = eventScheduleFormSet(
            queryset=schedules,
            initial=[{'dateFrom':datetime.date.today(),
                      'timeFrom':'00:00',
                      'timeTo':'00:00'
        }])

    return render_event(request, {
                                    "eventSchedules": eventSchedules,
                                    "eventForm": eventForm
                                 })
    pass

"""
@login_required
@permission_required('publisher.publish')
def credit(request, eventId):
    event = Event.objects.select_related('blogs').get(pk=eventId)

    if event.author != request.user:
        raise Event.DoesNotExist(_("You don't have permission to edit this event"))
    
    if request.method == "POST":
        addresses = []
        if request.POST.has_key(u"adr_id"):
            addressIds = request.POST.getlist('adr_id')
            for id in addressIds:
                if id == '': continue
                addresses.append(Address.objects.get(pk=id))
        eventForm = NewEventForm(request.user, request.POST, request.FILES, instance=event)
        if eventForm.is_valid():
            eventForm.saveEvent(request, addresses)
            messages.success(request, ugettext("Event details successfully changed."))
    else:
        eventForm = NewEventForm(request.user, instance=event)
        addresses = []#event.addresses.all()
    
    return render_event(request,{
                                    "eventForm":eventForm,
                                    "addresses":addresses
                                })
"""

def manage(request):
    myEvents = Event.objects.filter(author=request.user)
    return render_to_response("events/events_manage.html",
                              {
                                "myEvents": myEvents,
                              },
                              context_instance=RequestContext(request)
                              )

def main(request):
    events = Event.objects.all().order_by('dateFrom','rating')
    return render_to_response("events/events_main.html",
                              {
                                    "events": events
                              },
                              context_instance=RequestContext(request)
                              )

