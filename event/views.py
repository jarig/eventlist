import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Count
from django.forms.models import  modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext
from event.forms import EventForm, EventScheduleForm, EventScheduleFormSet
from event.models import Event, EventSchedule, EventGo
from party.forms import CreateSimplePartyForm


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
        if len(schedules):
            extraSchedule = 0
    
    eventScheduleFormSet = modelformset_factory(EventSchedule,
                                                form=EventScheduleForm,
                                                formset=EventScheduleFormSet, can_delete=True, extra=extraSchedule)
    if request.method == "POST":
        eventForm = EventForm(request.user, request.POST, request.FILES,instance=event)
        eventSchedules = eventScheduleFormSet(request.POST,
                                              queryset=schedules)
        if eventForm.is_valid() and eventSchedules.is_valid():
            newEvent = eventForm.saveEvent(request, eventSchedules)
            messages.success(request, ugettext("Event successfully created"))
            #redirect to edit/publish event
            return HttpResponseRedirect(reverse("event.views.credit", kwargs={"event": newEvent.id}))
    else:
        eventForm = EventForm(request.user, instance=event)
        eventSchedules = eventScheduleFormSet(
            queryset=schedules,
            #initial=[{'dateFrom':datetime.date.today(),
            #          'timeFrom':'00:00',
            #          'timeTo':'00:00'
        #}]
        )

    return render_event(request, {
                                    "eventSchedules": eventSchedules,
                                    "eventForm": eventForm
                                 })
    pass

def manage(request):
    myEvents = Event.objects.filter(author=request.user)
    return render_to_response("events/events_manage.html",
                              {
                                "myEvents": myEvents,
                              },
                              context_instance=RequestContext(request)
                              )



def main(request):
    eventSchedules = EventSchedule.objects.all().order_by("-dateFrom", "-timeFrom")
    eventSchedules = eventSchedules.extra(select={'goes':
                                                      "SELECT true FROM dual WHERE EXISTS ( SELECT id FROM %s WHERE user_id=%d and id=%s.`event_id`)" % ( EventGo._meta.db_table, request.user.pk, EventSchedule._meta.db_table) })
    print eventSchedules.query
    createPartyFormSample = CreateSimplePartyForm(
        initial={
            "author":request.user
        }
    )
    return render_to_response("events/events_main.html",
                              {
                                    "eventSchedules": eventSchedules,
                                    "createPartyFormSample": createPartyFormSample
                              },
                              context_instance=RequestContext(request)
                              )

@login_required
def go(request, eventSchId):
    goObj = _go(request.user, eventSchId)
    return HttpResponse("id="+goObj.pk)


def _go(user, eventSchId):
    """
    Record user as event participant
    """
    return EventGo.objects.get_or_create(eventSchedule=EventSchedule.objects.get(pk=eventSchId), user=user)

def _unGo(user, eventSchId):
    EventGo.objects.filter(pk=eventSchId,user=user).delete()
    return True