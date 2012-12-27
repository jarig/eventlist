import datetime
from django.db import models
import time
from _ext.pibu.fields import ImagePreviewModelField
from account.models import Account
from blog.models import Blog
from common.models import Address
from event.managers import EventManager
from organization.models import Organization

# activities(categories) available for events
class EventActivity(models.Model):
    name = models.CharField(max_length=128)
    icon = models.ImageField(upload_to="event/event_type/icon/", blank=True, default='')
    thumbnail = models.ImageField(upload_to="event/event_type/thumb/", blank=True, default='')
    thumbnail_128 = models.ImageField(upload_to="event/event_type/thumb128/", blank=True, default='')
    parent = models.ForeignKey('EventActivity', blank=True, null=True, editable=False) #not null if subcategory
    confirmed = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name
    class Meta:
        unique_together = ('name',)

#todo invalidate cache
def event_logo_name(instance, filename):
    return "event/logo/main_logo_%d" % int(time.time())
#
class Event(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(Account)
    logo = ImagePreviewModelField(upload_to=event_logo_name,max_height=300, max_width=300)
    # blogs/pages on which this event is published, derive from EventSchedule blog fields
    blogs = models.ManyToManyField(Blog, blank=True, null=True, editable=False) #optimization field
    activities = models.ManyToManyField(EventActivity, blank=True, null=True, related_name='activities') #event activities/actions
    organizers = models.ManyToManyField(Organization, related_name='organizers') # organizations that are responsible for this event
    descr = models.TextField() #event description (with BB code)
    rating = models.FloatField(default=0,editable=False) #event rating
    created = models.DateTimeField(auto_now_add=True, editable=False) #date event created
    participants = models.PositiveIntegerField(default=0, editable=False) # number of participants, help num (not exact)
    confirmed = models.BooleanField(editable=False, default=True) #event confirmed by blog/page admins

    #dateFrom - first schedule dateFrom
    #dateTo - last schedule dateTo
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
    classifier = models.CharField(max_length=255,default='',blank=True) #aux. data for term ( like currency, age, etc. )

# table to record 'goes' for each event schedule
# TODO add go for event
class EventGo(models.Model):
    eventSchedule = models.ForeignKey(EventSchedule, editable=False)
    #event = models.ForeignKey(EventSchedule, editable=False) # for performance
    user = models.ForeignKey(Account, editable=False, related_name='goesOnEvents')
    created = models.DateTimeField(auto_now_add=True) #go created

    class Meta:
        unique_together = ('eventSchedule', 'user')

    @staticmethod
    def getGoesStatement(user):
        if not user or user.is_anonymous(): return 0
        goes = "SELECT 1 FROM dual WHERE EXISTS ( SELECT id FROM %s WHERE %s=%d and %s=SCH.`id` LIMIT 1)" %\
               ( EventGo._meta.db_table,
                 EventGo.user.field.column,
                 user.pk,
                 EventGo.eventSchedule.field.column)
        return goes

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
