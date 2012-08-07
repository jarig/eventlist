from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.forms.models import  modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from account.models import Account
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
                                              queryset=schedules, prefix="eventForm")
        if eventForm.is_valid() and eventSchedules.is_valid():
            newEvent = eventForm.saveEvent(request, eventSchedules)
            messages.success(request, _("Event successfully created"))
            #redirect to edit/publish event
            return HttpResponseRedirect(reverse("event.views.credit", kwargs={"event": newEvent.id}))
    else:
        eventForm = EventForm(request.user, instance=event)
        eventSchedules = eventScheduleFormSet(
            queryset=schedules,
            prefix="eventForm"
        )

    return render_event(request, {
                                    "eventSchedules": eventSchedules,
                                    "eventForm": eventForm
                                 })
    pass



def view_schedule(request,scheduleId):
    try:
        schedule = EventSchedule.objects.select_related('event','address').get(pk=scheduleId)
        friends = Account.objects.filter(pk__in=EventGo.objects.filter(eventSchedule=schedule).values("user"))[:11]
    except EventSchedule.DoesNotExist:
        return HttpResponseNotFound(_("Such event doesn't exist"))

    return render_to_response("event/events_view_schedule.html",
        {
            "schedule": schedule,
            "friends": friends
        },
        context_instance=RequestContext(request)
    )

def manage(request):
    myEvents = Event.objects.filter(author=request.user)
    return render_to_response("event/events_manage.html",
                              {
                                "myEvents": myEvents,
                              },
                              context_instance=RequestContext(request)
                              )


#show main events
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

    eventSchedules = EventSchedule.objects.raw("""select EE.*, SCH.*,
                                                (%s) AS `goes`
                                                FROM  %s EE,
                                                (SELECT * FROM %s SC GROUP BY %s ORDER BY dateFrom DESC) as SCH
                                                WHERE EE.id=SCH.%s ORDER BY SCH.dateFrom DESC""" % (
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


# ========= AJAX views ============
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

def searchEvent(request):
    events = Event.objects.latest_schedules(limit=10)
    return render_to_response("event_search.html",
            {
            'events': events
        },
        context_instance=RequestContext(request)
    )
# ======= AJAX views END ==========