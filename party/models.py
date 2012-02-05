from django.contrib.auth.models import User
from django.db import models
from common.models import Address
from event.models import Event

class Party(models.Model):
    #author = models.ForeignKey(User,related_name='authorOfParties')
    #members = models.ManyToManyField(User, through='PartyMember', editable=False)
    #party options
    closed=models.BooleanField(default=False, editable=False)
    #
    created=models.DateTimeField(auto_now_add=True, editable=False)
    pass #party model

# party schedules
class PartySchedule(models.Model):
    party = models.ForeignKey(Party, related_name='schedules')
    location = models.ForeignKey(Address)
    dateFrom = models.DateField(null=True, blank=True) #date when party starts/gathers
    timeFrom = models.TimeField(null=True, blank=True)
    dateTo = models.DateField(null=True, blank=True) #date when party ends
    timeTo = models.TimeField(null=True, blank=True)
    pass

class PartyMember(models.Model):
    class ROLE:
        OWNER = 30
        MODERATOR = 20
        PARTICIPANT = 10
        CANDIDATE = 1
    _ROLE_CHOICES = (
        (ROLE.OWNER,u'owner'),
        (ROLE.MODERATOR,u'moderator'),
        (ROLE.PARTICIPANT,u'participant'),
        (ROLE.CANDIDATE, u'candidate'),
    )
    party = models.ForeignKey(Party, related_name='members')
    user = models.ForeignKey(User, related_name='partyMembership')
    role = models.PositiveIntegerField(choices=_ROLE_CHOICES, default=1)
    
    dateAdded = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('party', 'user')
    pass

class PartyEvent(models.Model):
    party = models.ForeignKey(Party)
    event = models.ForeignKey(Event, null=True, blank=True)
    url = models.CharField(max_length=1024, default="", blank=True)
    
    
    pass