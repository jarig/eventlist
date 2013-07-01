from django.core.files.storage import DefaultStorage
from django.db import models
from django.utils.translation import ugettext_lazy
from account.models import Account
from _ext.pibu.fields import ImagePreviewModelField
from blog.models import Blog
from common.models import Address, Language
from event.models import Event, EventSchedule

class Party(models.Model):
    name = models.CharField(max_length=255, editable=False) #same as event name by default
    author = models.ForeignKey(Account, related_name='authorOfParties', editable=False)
    logo = ImagePreviewModelField(upload_to="party/logo/", null=True, blank=True)
    description = models.TextField(blank=True, default='')
    #party options
    closed=models.BooleanField(default=True)#if opened, then logo, description should exist
    #
    created=models.DateTimeField(auto_now_add=True, editable=False)

    eventSchedule = models.ForeignKey(EventSchedule, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    dateFrom = models.DateField(null=True, blank=True) #date when party starts/gathers
    timeFrom = models.TimeField(null=True, blank=True)
    dateTo = models.DateField(null=True, blank=True) #date when party ends
    timeTo = models.TimeField(null=True, blank=True)

    #autofilled fields ( for optimization )
    event = models.ForeignKey(Event, editable=False, null=True, blank=True)
    blog = models.ForeignKey(Blog, null=True, blank=True, editable=False)
    address = models.ForeignKey(Address, editable=False, null=True, blank=True)


    def __unicode__(self):
        return unicode(self.name)

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