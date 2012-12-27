from django.db import transaction
from account.models import Account
from event.models import EventSchedule
from event.views import _go
from party.models import PartyMember, Party


def createPartyForEvent(user, eventScheduleId):
    eventSch = EventSchedule.objects.select_related('event').get(pk=eventScheduleId)
    #check that it doesnt exist already
    parties = Party.objects.filter(schedules__eventSchedule=eventScheduleId, author=user).all()
    if len(parties):
        if len(parties) == 1:
            return parties[0], None, None
        else:
            #TODO multiple parties organized by 1 user for the same event schedule
            pass
    _go(user,eventSch)
    party = Party.objects.create(author=user)
    partySched = Party.objects.create(party=party,
                                                name=eventSch.event.name,
                                                location=eventSch.address,
                                                dateFrom=eventSch.dateFrom,
                                                timeFrom=eventSch.timeFrom,
                                                eventSchedule=eventSch,
                                                dateTo=eventSch.dateTo,
                                                timeTo=eventSch.timeTo)
    partyMemberShip = PartyMember.objects.create(user=user,
                                                party=party,
                                                role=PartyMember.ROLE.OWNER)

    return party, partySched, partyMemberShip

@transaction.commit_manually
def invitePeopleToParty(party, people):
    for person in people:
        member, created = PartyMember.objects.get_or_create(party=party, user=Account(pk=person), defaults={'role': PartyMember.ROLE.INVITED})
    transaction.commit()
    pass
