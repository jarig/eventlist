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
from event.models import Event, EventSchedule, EventGo, EventActivity
from party.forms import CreatePartyForm
from search.forms import FastSearchForm


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
    #TODO reduce queries
    try:
        schedule = EventSchedule.objects.select_related('event','address','blog').get(pk=scheduleId)
        schedule.goes = False
        if request.user.is_authenticated():
            schedule.goes = EventGo.objects.filter(eventSchedule=schedule, user=request.user).exists()
        friends = []
        if request.user.is_authenticated():
            friends = request.user.friends.filter(pk__in=EventGo.objects.all().values("user"))
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
    if request.user.is_authenticated():
        createPartyFormSample = CreatePartyForm(
            initial={
                "author":request.user
            }
        )

    search = "1=1" #search statement
    params = []
    if request.GET:
        fastSearchForm = FastSearchForm(request.GET)
        if fastSearchForm.is_valid():
            search = "EE.name LIKE %(searchToken)s "
            params = { 'searchToken' : '%'+fastSearchForm.cleaned_data["search"]+'%' }
    else:
        fastSearchForm = FastSearchForm()

    eventSchedules = EventSchedule.objects.raw("""select EE.*, SCH.*,
                                                (%s) AS `goes`
                                                FROM  %s EE,
                                                (SELECT *, (dateFrom <= NOW()) as started FROM %s SC WHERE dateTo >= NOW() ORDER BY started, dateFrom ) as SCH
                                                WHERE EE.id=SCH.%s and %s ORDER BY SCH.started, SCH.dateFrom""" % (
                                                                          EventGo.getGoesStatement(request.user),
                                                                          Event._meta.db_table,
                                                                          EventSchedule._meta.db_table,
                                                                          EventSchedule.event.field.column,
                                                                          search), params=params)

    return render_to_response("event/events_main.html",
                              {
                                    "eventSchedules": eventSchedules,
                                    "createPartyFormSample": createPartyFormSample,
                                    "fastSearchForm": fastSearchForm
                              },
                              context_instance=RequestContext(request)
                              )

def byActivity(request):
    activities = EventActivity.objects.filter(parent=None, confirmed=True)
    return render_to_response("event/events_activities.html",
        {
            "eventActivities": activities,
        },
        context_instance=RequestContext(request)
    )

def showActivityCategory(request, activityName):
    events = Event.objects.raw("""select EE.* from %(activityM2MTable)s  EEA, %(eventTable)s EE, %(eventActivityTable)s EACT
                                 WHERE EEA.%(m2mEventId)s=EE.id and EEA.%(m2mActivityId)s=EACT.id and EACT.name=%(activityName)s""" %
                                {'activityM2MTable': Event.activities.through._meta.db_table,
                                 'eventTable':Event._meta.db_table,
                                 'eventActivityTable': EventActivity._meta.db_table,
                                 'm2mEventId':Event.activities.through.event.field.column,
                                 'm2mActivityId':Event.activities.through.eventactivity.field.column,
                                 'activityName':'%s'},
                                params=(activityName,))
    return render_to_response("event/events_event_list.html",
        {
            "events": events,
            },
        context_instance=RequestContext(request)
    )
    pass

# ========= AJAX views ============
@login_required
def go(request, eventSchId):
    goObj, created = _go(request.user, EventSchedule.objects.get(pk=eventSchId))
    return HttpResponse("{id: %d}" % goObj.pk)

@login_required
def unGo(request, eventSchId):
    return HttpResponse(str(_unGo(request.user, eventSchId)))

def _go(user, eventSch):
    """
    Record user as an event participant
    """
    return EventGo.objects.get_or_create(eventSchedule=eventSch, user=user)

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