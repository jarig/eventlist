# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.http import HttpResponse
from event.models import Event, EventSchedule
from event.views import _go
from party.forms import CreateSimplePartyForm
from party.models import Party, PartySchedule, PartyMember

@login_required
def silentCreateWithEvent(request, eventScheduleId):
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
    data= json.simplejson.dumps({ "id": party.pk, "schedule": partySched.pk, "membership": partyMemberShip.pk })
    return HttpResponse(data)
    #return HttpResponse(json.simplejson.dumps({ "error": { "id": 1, "message":"Invalid request" }}))
    pass
