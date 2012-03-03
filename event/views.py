import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Count
from django.db.models.expressions import F
from django.forms.models import  modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext
from event.forms import EventForm, EventScheduleForm, EventScheduleFormSet
from event.models import Event, EventSchedule, EventGo
from party.forms import CreatePartyForm


def render_event(request, attrs):

    return render_to_response("event/events_credit.html",
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
        )

    return render_event(request, {
                                    "eventSchedules": eventSchedules,
                                    "eventForm": eventForm
                                 })
    pass

def manage(request):
    myEvents = Event.objects.filter(author=request.user)
    return render_to_response("event/events_manage.html",
                              {
                                "myEvents": myEvents,
                              },
                              context_instance=RequestContext(request)
                              )



def main(request):
    createPartyFormSample = None
    goes = "0"
    if request.user.is_authenticated():
        createPartyFormSample = CreatePartyForm(
            initial={
                "author":request.user
            }
        )
        goes = "SELECT 1 FROM dual WHERE EXISTS ( SELECT id FROM %s WHERE %s=%d and %s=SCH.`id`)" %\
               ( EventGo._meta.db_table,
                 EventGo.user.field.column,
                 request.user.pk,
                 EventGo.eventSchedule.field.column)

    eventSchedules = EventSchedule.objects.raw("""select SCH.*,
                                                (%s) AS `goes`
                                                FROM  %s EE,
                                                (SELECT * FROM %s SC GROUP BY %s ORDER BY dateFrom DESC) as SCH
                                                WHERE EE.id=SCH.%s """ % (
                                                                          goes,
                                                                          Event._meta.db_table,
                                                                          EventSchedule._meta.db_table,
                                                                          EventSchedule.event.field.column,
                                                                          EventSchedule.event.field.column))

    return render_to_response("event/events_main.html",
                              {
                                    "eventSchedules": eventSchedules,
                                    "createPartyFormSample": createPartyFormSample
                              },
                              context_instance=RequestContext(request)
                              )

@login_required
def go(request, eventSchId):
    goObj, created = _go(request.user, EventSchedule.objects.get(pk=eventSchId))
    return HttpResponse("{id: %d}" % goObj.pk)


def _go(user, eventSch):
    """
    Record user as an event participant
    """
    return EventGo.objects.get_or_create(eventSchedule=eventSch, user=user)

def unGo(request, eventSchId):
    return HttpResponse(str(_unGo(request.user, eventSchId)))

def _unGo(user, eventSchId):
    EventGo.objects.filter(eventSchedule=eventSchId,user=user).delete()
    return True