import datetime
from django.db import models
import time
from _ext.pibu.fields import ImagePreviewModelField
from account.models import Account
from blog.models import Blog
from common.models import Address
from event.managers import EventManager
from organization.models import Organization

# activities available for events
class EventActivity(models.Model):
    name = models.CharField(max_length=128)
    icon = models.ImageField(upload_to="event/event_type/icon/", blank=True, default='')
    thumbnail = models.ImageField(upload_to="event/event_type/thumb/", blank=True, default='')
    confirmed = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name
    class Meta:
        unique_together = ('name',)


def event_logo_name(instance, filename):
    return "event/logo/main_logo_%d" % int(time.time())
#
class Event(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(Account)
    logo = ImagePreviewModelField(upload_to=event_logo_name,max_height=300, max_width=300)
    # blogs/pages on which this event is published, derive from EventSchedule blog fields
    blogs = models.ManyToManyField(Blog, blank=True, null=True, editable=False)
    activities = models.ManyToManyField(EventActivity, blank=True, null=True) #event activities/actions
    organizers = models.ManyToManyField(Organization) # organizations that are responsible for this event
    descr = models.TextField() #event description (with BB code)
    rating = models.FloatField(default=0) #event rating
    created = models.DateTimeField(auto_now_add=True) #date event created
    participants = models.PositiveIntegerField(default=0) # number of participants, help num (not exact)
    confirmed = models.BooleanField(editable=False, default=True) #event confirmed by blog/page admins

    objects = EventManager()

    def __unicode__(self):
        return u"%s" % self.name
    
# Event may have many schedules
class EventSchedule(models.Model):
    event = models.ForeignKey(Event, editable=False,related_name='schedules')
    dateFrom = models.DateField(default=datetime.date.today) #date when event starts
    timeFrom = models.TimeField(default='00:00')
    dateTo = models.DateField(null=True, blank=True, default=datetime.date.today) #date when event ends
    timeTo = models.TimeField(default='00:00', null=True, blank=True)
    address = models.ForeignKey(Address, null=True, related_name='eventSchedules') #location where this event is held
    blog = models.ForeignKey(Blog, null=True, blank=True, default=None, related_name='eventSchedules') # blog's address
    created = models.DateTimeField(auto_now_add=True) #date created

    def __unicode__(self):
        return ("%s %s") % (self.event.name, self.dateFrom.strftime('%d/%m/%Y'))

# Terms to be applied for each eventSchedule, can be none
class EventTerms(models.Model):
    class Conditions:
        AGE = 'A'
        PRICE = 'P'
    _CONDITIONS = (
        (Conditions.AGE,u'age'),
        (Conditions.PRICE,u'price'),
    )
    eventSchedule = models.ForeignKey(EventSchedule, editable=False, related_name='terms')
    type = models.CharField(choices=_CONDITIONS, max_length=2, default=Conditions.PRICE)
    min_value = models.IntegerField(null=True, blank=True)
    max_value = models.IntegerField(null=True, blank=True)
    classifier = models.CharField(max_length=255,default='',blank=True) #aux. data for term ( like currency, etc. )

# table to record 'goes' for each event schedule
# TODO add go for event
class EventGo(models.Model):
    eventSchedule = models.ForeignKey(EventSchedule, editable=False)
    #event = models.ForeignKey(EventSchedule, editable=False) # for performance
    user = models.ForeignKey(Account, editable=False, related_name='goesOnEvents')
    created = models.DateTimeField(auto_now_add=True) #go created

    class Meta:
        unique_together = ('eventSchedule', 'user')

# event comments
class Comment(models.Model):
    COMMENT_TYPE = (
        (u'P',u'positive'),
        (u'N',u'negative'),
        (u'U',u'neutral')
    )
    event = models.ForeignKey(Event)
    author = models.ForeignKey(Account)
    type = models.CharField(max_length=1, choices=COMMENT_TYPE, default='U')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True) #created
    
#
class Invite(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(Account, related_name='invites')
    person = models.ForeignKey(Account, related_name='invited')
    created = models.DateTimeField(auto_now_add=True) #created

    class Meta:
        unique_together = ('event', 'user', 'person')
