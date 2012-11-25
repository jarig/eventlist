# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.core.urlresolvers import resolve, reverse
from django.core.validators import validate_slug, RegexValidator
from django.db import transaction
from django.db.models.query_utils import Q
from django.forms.models import modelformset_factory
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext
from account.models import Account
from event.models import EventSchedule
from party.forms import CreatePartyForm, CustomPartyScheduleForm, EventPartyScheduleForm, PartyScheduleFormSet
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
def create(request):
    return _credit(request)
    pass

@login_required
def edit(request, party):
    #TODO check perms
    party = Party(pk=party)
    return _credit(request, party=party)

def _credit(request, initialCreatePartyForm=None, initialEventSchedulesFormSet=None, party=None):
    pSchedules = PartySchedule.objects.none()
    invited = []
    if party:
        pSchedules = party.schedules.all()
        invited = party.members.all()
    extraPartySched = 1
    if len(pSchedules):
        extraPartySched = 0

    CustomPartySheduleSet = modelformset_factory(PartySchedule,
                                                    form=CustomPartyScheduleForm,
                                                    formset=PartyScheduleFormSet,
                                                    extra=extraPartySched,can_delete=True, can_order=True)

    if request.POST:
        invited = request.POST.getlist("invited")
        createPartyForm = CreatePartyForm(request.POST, instance=party)
        customPartyScheduleFormSet = CustomPartySheduleSet(request.POST, queryset=pSchedules)
        if createPartyForm.is_valid() and customPartyScheduleFormSet.is_valid():
            party = createPartyForm.saveParty(request.user, customPartyScheduleFormSet, invited)
            messages.success(request, ugettext("Party successfully created"))
            return HttpResponseRedirect(reverse('party.views.edit', kwargs={'party':party.pk}))
    else:
        createPartyForm = CreatePartyForm(initial=initialCreatePartyForm,instance=party)
        customPartyScheduleFormSet = CustomPartySheduleSet(initial=initialEventSchedulesFormSet, queryset=pSchedules)

    return render_to_response("party/party_credit.html",
            {
            "createPartyForm": createPartyForm,
            "invited": invited,
            "customPartyScheduleFormSet": customPartyScheduleFormSet,
            "party": party
        },
        context_instance=RequestContext(request)
    )


@login_required
def manage(request):
    #TODO reduce too many queries
    partyMembership = []
    _partyMembership =  request.user.partyMembership.all().select_related('party')
    for _member in _partyMembership:
        partyMembers = PartyMember.objects.filter(Q(party=_member.party) & ~Q(user=request.user)).select_related('user').all()[:10]
        _member.partyMembers = partyMembers
        partyMembership.append(_member)

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
def invitationList(request, eventScheduleId):
    if request.POST:
        friends = request.POST.getlist('friends[]')
        if len(friends):
            with transaction.commit_on_success():
                party, partySched, partyMembership = createPartyForEvent(request.user, eventScheduleId)
                invitePeopleToParty(party, friends)
            return HttpResponse('done')
    else:
        invited = []
        exclude = []
        if request.POST:#TODO filter out friends that already added
            exclude = request.POST.getlist("exclude[]",[])
        #TODO take only mutual friends
        friendships = request.user.friends.all().extra(select={'date_added': "account_friendship.date_added"}).order_by("-date_added")
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
