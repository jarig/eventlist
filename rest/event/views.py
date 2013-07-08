from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.cache import get_cache
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from haystack.query import SearchQuerySet
from account.models import Account
from event.forms import EventForm, EventScheduleForm, EventScheduleFormSet
from event.models import Event, EventSchedule, EventGo, EventActivity, EventGroup
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
        eventForm = EventForm(request.user, request.POST, request.FILES, instance=event)
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


def view_schedule(request, scheduleId):
    #TODO reduce queries
    try:
        schedule = EventSchedule.objects.select_related('event', 'address', 'blog').get(pk=scheduleId)
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
def showEvents_old(request):
    createPartyFormSample = None
    if request.user.is_authenticated():
        createPartyFormSample = CreatePartyForm(
            initial={
                "author": request.user
            }
        )

    search = "1=1 "  # search statement
    addTables = ""
    params = {}
    if request.GET:
        fastSearchForm = FastSearchForm(request.GET)
        if fastSearchForm.is_valid():
            if fastSearchForm.cleaned_data["search"]:
                search += "AND EE.name LIKE %(searchToken)s "
                params['searchToken'] = '%' + fastSearchForm.cleaned_data["search"] + '%'
            if fastSearchForm.cleaned_data["category"]:
                addTables += "event_event_activities EEA, event_eventactivity EA"
                search += "AND EEA.event_id=EE.id AND EEA.eventactivity_id=EA.id AND EA.group_id=%(category)s "
                params['category'] = fastSearchForm.cleaned_data["category"].pk
                #TODO: use elasticSearch
            events = SearchQuerySet().filter(groups=fastSearchForm.cleaned_data["category"].name).models(Event)
            print "Elastic events: %s" % events
    else:
        fastSearchForm = FastSearchForm()
    #TODO: optimization, add isActive check instead of dateFrom checks
    eventSchedules = EventSchedule.objects.raw("""select EE.*, SCH.*,
                                                (%s) AS `goes`
                                                FROM  %s EE, %s
                                                (SELECT *, (dateFrom <= NOW()) as started FROM %s SC WHERE dateTo >= NOW() ORDER BY started, dateFrom ) as SCH
                                                WHERE EE.id=SCH.%s and %s ORDER BY SCH.started, SCH.dateFrom""" % (
        EventGo.getGoesStatement(request.user),
        Event._meta.db_table,
        addTables + ("," if addTables else ""),
        EventSchedule._meta.db_table,
        EventSchedule.event.field.column,
        search), params=params)
    #print eventSchedules.query



    return render_to_response("event/events_main.html",
                              {
                                  "eventSchedules": eventSchedules,
                                  "createPartyFormSample": createPartyFormSample,
                                  "fastSearchForm": fastSearchForm
                              },
                              context_instance=RequestContext(request)
    )


def showEvents(request):
    #TODO: change to class based view
    eventSchedules = None
    createPartyFormSample = None
    if request.user.is_authenticated():
        createPartyFormSample = CreatePartyForm(
            initial={
                "author": request.user
            }
        )
    if request.GET:
        fastSearchForm = FastSearchForm(request.GET)
        if fastSearchForm.is_valid():
            events = fastSearchForm.search()
            print "Elastic events: %s" % events
    else:
        fastSearchForm = FastSearchForm()

    return render_to_response("event/events_main.html",
                              {
                                  "eventSchedules": eventSchedules,
                                  "createPartyFormSample": createPartyFormSample,
                                  "fastSearchForm": fastSearchForm
                              },
                              context_instance=RequestContext(request)
    )
    pass


def showEventGroups(request):
    """
        Show events in groups
    """
    if request.GET:
        fastSearchForm = FastSearchForm(request.GET)
        if fastSearchForm.is_valid():
            #fastSearchForm.cleaned_data["search"]
            return showEvents(request)
        #redirect to /event page
    else:
        fastSearchForm = FastSearchForm()

    #get groups

    cache = get_cache("longMem")
    groups = EventGroup.objects.filter(featured=False)
    for group in groups:
        events = cache.get("group_thumb_event_%s" % group.pk)
        if events is None or not len(events):
            events = Event.objects.filter(activities__group=group)[:3]
            cache.set("group_thumb_event_%s" % group.pk, events, 60*30)  # 30min
        group.events = events

    return render_to_response("event/events_event_groups.html",
                              {
                                  "groups": groups,
                                  "fastSearchForm": fastSearchForm
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
    EventGo.objects.filter(eventSchedule=eventSchId, user=user).delete()
    return True
    # ======= AJAX views END ==========