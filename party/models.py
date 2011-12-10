from django.contrib.auth.models import User
from django.db import models
from event.models import Event

class Party(models.Model):

    members = models.ManyToManyField(User, through='PartyMember', editable=False)
    max_members=models.PositiveIntegerField(default=2)
    closed=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    pass #party model


class PartyMember(models.Model):
    ROLE = (
        (30,u'owner'),
        (20,u'moderator'),
        (10,u'participant'),
        (1, u'candidate'),
    )
    party = models.ForeignKey(Party)
    user = models.ForeignKey(User)
    role = models.PositiveIntegerField(choices=ROLE, default=1)
    
    dateAdded = models.DateTimeField(auto_now_add=True)
    pass

class PartyEvent(models.Model):
    party = models.ForeignKey(Party)
    event = models.ForeignKey(Event, null=True, blank=True)
    url = models.CharField(max_length=1024, default="", blank=True)
    
    
    pass