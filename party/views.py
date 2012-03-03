# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.forms.models import modelformset_factory
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext
from event.models import EventSchedule
from event.views import _go
from party.forms import CreatePartyForm
from party.models import Party, PartySchedule, PartyMember

@login_required
def forEvent(request, eventScheduleId):
    # automatically create 1 party schedule binded to eventScheduleId
    # party name == event name
    #
    eventSch = EventSchedule.objects.get(pk=eventScheduleId)
    createForm ={
        'name': ugettext("Party for ")+eventSch.event.name
    }
    partyShedules = [
            {
            'eventSchedule': eventSch,
            'dateFrom': eventSch.dateFrom,
            'timeFrom': eventSch.timeFrom,
            'dateTo': eventSch.dateTo,
            'timeTo': eventSch.timeTo,
            'location': eventSch.address,
        }
    ]

    return _credit(request, createForm, partyShedules)
    pass

@login_required
def credit(request):

    return _credit(request)
    pass


def _credit(request, initialCreatePartyForm=None, initialEventSchedulesFormSet=None, party=None):
    PartySheduleSet = modelformset_factory(PartySchedule)
    pSchedules = None
    if party: pSchedules = party.schedules

    if request.POST:
        createPartyForm = CreatePartyForm(request.POST, instance=party)
        eventSchedulesFormSet = PartySheduleSet(request.POST, queryset=pSchedules)
    else:
        createPartyForm = CreatePartyForm(initial=initialCreatePartyForm,instance=party)
        eventSchedulesFormSet = PartySheduleSet(initial=initialEventSchedulesFormSet, queryset=pSchedules)


    return render_to_response("party/party_credit.html",
            {
            "createPartyForm": createPartyForm,
            "eventSchedulesFormSet": eventSchedulesFormSet,
        },
        context_instance=RequestContext(request)
    )


@login_required
def manage(request):
    partyMembership =  request.user.partyMembership.all().select_related('party')
    return render_to_response("party/party_manage.html",
            {
            "partyMembership": partyMembership
        },
        context_instance=RequestContext(request)
    )
    pass

@login_required
def inviteToEvent(request, eventScheduleId):
    #record to event go
    eventSch = EventSchedule.objects.get(pk=eventScheduleId)
    _go(request.user,eventSch)
    party = Party.objects.create()
    partySched = PartySchedule.objects.create(party=party,
                                              location=eventSch.address,
                                              dateFrom=eventSch.dateFrom,
                                              timeFrom=eventSch.timeFrom,
                                              dateTo=eventSch.dateTo,
                                              timeTo=eventSch.timeTo)
    partyMemberShip = PartyMember.objects.create(user=request.user,
                                                 party=party,
                                                 role=PartyMember.ROLE.OWNER)


    data = json.simplejson.dumps({ "id": party.pk, "schedule": partySched.pk, "membership": partyMemberShip.pk })
    pass

def getInvitationList(request):

    return render_to_response("party_friend_list.html",
            {
            },
        context_instance=RequestContext(request)
    )
