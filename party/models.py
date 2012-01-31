from django.contrib.auth.models import User
from django.db import models
from common.models import Address
from event.models import Event

class Party(models.Model):
    author = models.ForeignKey(User,related_name='authorOfParties')
    members = models.ManyToManyField(User, through='PartyMember', editable=False)
    closed=models.BooleanField(default=False, editable=False)
    created=models.DateTimeField(auto_now_add=True, editable=False)
    pass #party model

# party schedules
class PartySchedule(models.Model):
    party = models.ForeignKey(Party)
    location = models.ForeignKey(Address)
    dateFrom = models.DateField(null=True, blank=True) #date when party starts/gathers
    timeFrom = models.TimeField(null=True, blank=True)
    dateTo = models.DateField(null=True, blank=True) #date when party ends
    timeTo = models.TimeField(null=True, blank=True)
    pass

class PartyMember(models.Model):
    ROLE = (
        (30,u'owner'),
        (20,u'moderator'),
        (10,u'participant'),
        (1, u'candidate'),
    )
    party = models.ForeignKey(Party, related_name='+')
    user = models.ForeignKey(User, related_name='partyMembership')
    role = models.PositiveIntegerField(choices=ROLE, default=1)
    
    dateAdded = models.DateTimeField(auto_now_add=True)
    pass

class PartyEvent(models.Model):
    party = models.ForeignKey(Party)
    event = models.ForeignKey(Event, null=True, blank=True)
    url = models.CharField(max_length=1024, default="", blank=True)
    
    
    pass