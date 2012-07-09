from django.core.files.storage import DefaultStorage
from django.db import models
from django.utils.translation import ugettext_lazy
from account.models import Account
from _ext.pibu.fields import ImagePreviewModelField
from common.models import Address, Language
from event.models import Event, EventSchedule

class Party(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True) #same as event name by default
    author = models.ForeignKey(Account, related_name='authorOfParties', editable=False)
    logo = ImagePreviewModelField(upload_to="party/logo/", null=True, blank=True)
    description = models.TextField(blank=True, default='')
    #party options
    closed=models.BooleanField(default=True)#if opened, then logo, description should exist
    #
    created=models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return unicode(self.name)

# party schedules == activity plans
class PartySchedule(models.Model):
    party = models.ForeignKey(Party, related_name='schedules', editable=False)
    location = models.ForeignKey(Address, verbose_name='Gathering Place') #gathering place
    eventSchedule = models.ForeignKey(EventSchedule, null=True, blank=True, related_name='partySchedules')
    url = models.URLField(verify_exists=False, null=True, blank=True)
    dateFrom = models.DateField(null=True, blank=True) #date when party starts/gathers
    timeFrom = models.TimeField(null=True, blank=True)
    dateTo = models.DateField(null=True, blank=True) #date when party ends
    timeTo = models.TimeField(null=True, blank=True)
    description = models.TextField(max_length=1024, blank=True, default='')
    pass

class PartyMember(models.Model):
    class ROLE:
        OWNER = 30
        MODERATOR = 20
        PARTICIPANT = 10
        INVITED = 2
        CANDIDATE = 1
    _ROLE_CHOICES = (
        (ROLE.OWNER,ugettext_lazy(u'Owner')),
        (ROLE.MODERATOR,ugettext_lazy(u'Moderator')),
        (ROLE.PARTICIPANT, ugettext_lazy(u'Participant')),
        (ROLE.INVITED, ugettext_lazy(u'Invited')),
        (ROLE.CANDIDATE, ugettext_lazy(u'Candidate')),
    )
    party = models.ForeignKey(Party, related_name='members')
    user = models.ForeignKey(Account, related_name='partyMembership')
    #userOutputName = models.CharField() # for efficiency
    role = models.PositiveIntegerField(choices=_ROLE_CHOICES, default=1)
    invitedBy = models.ForeignKey(Account, related_name='+', blank=True, null=True)

    dateAdded = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('party', 'user')

    def __unicode__(self):
        return unicode(self.user.first_name)
    pass

class MemberVacancy(models.Model):
    event = models.ForeignKey(Event)
    age_min = models.PositiveSmallIntegerField(null=True, blank=True)
    age_max = models.PositiveSmallIntegerField(null=True, blank=True)
    sex = models.CharField(choices=Account._SEX, max_length=1,null=True, blank=True)
    hasPhoto = models.NullBooleanField(null=True, blank=True)# true, false, null- doesnt matter
    language = models.ForeignKey(Language, null=True, blank=True)
    num = models.IntegerField(default=1) #number of such vacancies