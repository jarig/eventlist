from django.contrib.auth.models import User
from django.db import models
from event.models import Event

class Party(models.Model):
    author = models.ForeignKey(User,related_name='authorOfParties')
    members = models.ManyToManyField(User, through='PartyMember', editable=False)
    closed=models.BooleanField(default=False, editable=False)
    created=models.DateTimeField(auto_now_add=True, editable=False)
    #dateFrom = models.DateTimeField()
    #dateTo = models.DateTimeField()
    pass #party model


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