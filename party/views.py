# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.db import transaction
from django.db.models.query_utils import Q
from django.forms.models import modelformset_factory
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext
from event.models import EventSchedule
from party.forms import CreatePartyForm
from party.models import Party, PartySchedule, PartyMember
from party.utils import createPartyForEvent, invitePeopleToParty

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
    party, partySched, partyMemberShip = createPartyForEvent(request.user, eventScheduleId)
    data = json.simplejson.dumps({ "id": party.pk, "schedule": partySched.pk, "membership": partyMemberShip.pk })
    return HttpResponse(data)

@login_required
def getInvitationList(request, eventScheduleId):

    if request.POST:
        friends = request.POST.getlist('friends[]')
        if len(friends):
            with transaction.commit_on_success():
                party, partySched, partyMembership = createPartyForEvent(request.user, eventScheduleId)
                invitePeopleToParty(party, friends)
            return HttpResponse('done')
    else:
        invited = []
        #TODO take only mutual friends
        friendships = request.user.friends.all().select_related("friend").order_by('-date_added')
        try:
            party = Party.objects.get(schedules__eventSchedule=eventScheduleId, author=request.user)
            pMembers = party.members.filter(~Q(user = request.user)).select_related('user')
            for member in pMembers:
                invited.append(member.user)
        except Party.DoesNotExist:
            pass

        return render_to_response("party_invite_box.html",
                {
                "friendships": friendships,
                "invited": invited
                },
            context_instance=RequestContext(request)
        )
    return HttpResponseBadRequest('Bad request')
