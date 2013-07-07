import datetime
import uuid
from django.db import models
from _ext.pibu.fields import ImagePreviewModelField
from account.models import Account
from blog.models import Blog
from common.models import Address
from event.managers import EventManager
from organization.models import Organization


class EventGroup(models.Model):
    """
        Table for event groups
    """
    name = models.CharField(max_length=255)
    popularity = models.PositiveIntegerField(default=0, editable=False)  # automatically deducted value on daily basis
    featured = models.BooleanField(default=False,
                                   help_text="Defines if it's a special group which consist of manually added events.")

    def __unicode__(self):
        return self.name

    pass


# activities(categories) available for events
class EventActivity(models.Model):
    name = models.CharField(max_length=128)
    icon = models.ImageField(upload_to="event/event_type/icon/", blank=True, default='')
    thumbnail = models.ImageField(upload_to="event/event_type/thumb/", blank=True, default='')
    thumbnail_128 = models.ImageField(upload_to="event/event_type/thumb128/", blank=True, default='')
    parent = models.ForeignKey('EventActivity', blank=True, null=True, editable=False)  # not null if subcategory
    confirmed = models.BooleanField(default=False)
    # only ones that has parent=null may be attached to a group
    group = models.ForeignKey(EventGroup, blank=True, null=True,
                              related_name="activities",
                              help_text="Defines to which group should be assigned an event with such activity.")

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name',)


#todo invalidate cache
def event_logo_name(instance, filename):
    return "event/logo/ml_%s" % uuid.uuid4()


#
class Event(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(Account)
    logo = ImagePreviewModelField(upload_to=event_logo_name, max_height=300, max_width=300)
    # blogs/pages on which this event is published, derive from EventSchedule blog fields
    blogs = models.ManyToManyField(Blog, blank=True, null=True, editable=False,
                                   related_name='events')  # optimization field
    activities = models.ManyToManyField(EventActivity, blank=True, null=True,
                                        related_name='events')  # event activities/actions
    organizers = models.ManyToManyField(Organization,
                                        related_name='organizers')  # organizations that are responsible for this event
    descr = models.TextField()  # event description (with BB code)
    rating = models.FloatField(default=0, editable=False)  # event rating
    created = models.DateTimeField(auto_now_add=True, editable=False)  # date event created
    modified = models.DateTimeField(auto_now=True, editable=False, default=datetime.datetime.now)  # date event modified
    participants = models.PositiveIntegerField(default=0, editable=False) # number of participants, help num (not exact)
    confirmed = models.BooleanField(editable=False, default=True)  # event confirmed by blog/page admins

    objects = EventManager()

    def __unicode__(self):
        return u"%s" % self.name


# Event may have many schedules
class EventSchedule(models.Model):
    class STATUS:
        PENDING = 1
        IN_PROGRESS = 2
        PASSED = 3
    STATUS_CHOICES = (
        (STATUS.PENDING, "Pending"),
        (STATUS.IN_PROGRESS, "In Progress"),
        (STATUS.PASSED, "Passed"),
    )
    event = models.ForeignKey(Event, editable=False, related_name='schedules')
    dateFrom = models.DateField(default=datetime.date.today)  # date when event starts
    timeFrom = models.TimeField(default='00:00')
    dateTo = models.DateField(null=True, blank=True, default=datetime.date.today)  # date when event ends
    timeTo = models.TimeField(default='00:00', null=True, blank=True)
    # datetime till customer can enter the event, by default should be the same as dateFrom
    #enterTillTime = models.DateTimeField(default=datetime.date.today)
    shortDescription = models.CharField(max_length=1024, default='', blank=True)

    address = models.ForeignKey(Address, null=True, related_name='eventSchedules')  # location where this event is held
    blog = models.ForeignKey(Blog, null=True, blank=True, default=None, related_name='eventSchedules')  # blog's address
    created = models.DateTimeField(auto_now_add=True)  # date created
    modified = models.DateTimeField(auto_now=True, editable=False, default=datetime.datetime.now)  # date schedule modified
    #isActive = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, blank=True, null=True, editable=False)

    def __unicode__(self):
        return "%s %s %s" % (self.event.name, self.dateFrom.strftime('%d/%m/%Y'), self.timeFrom.strftime("%H:%M"))


# Terms to be applied for each event, can be none
class EventTerms(models.Model):
    class Conditions:
        AGE = 'A'
        PRICE = 'P'

    _CONDITIONS = (
        (Conditions.AGE, u'age'),
        (Conditions.PRICE, u'price'),
    )
    event = models.ForeignKey(Event, editable=False, related_name='terms')
    type = models.CharField(choices=_CONDITIONS, max_length=2, default=Conditions.PRICE)
    min_value = models.IntegerField(null=True, blank=True)
    max_value = models.IntegerField(null=True, blank=True)
    classifier = models.CharField(max_length=255, default='',
                                  blank=True) #aux. data for term ( like currency, measure units, etc. )
    modified = models.DateTimeField(auto_now_add=True, auto_now=True, editable=False,
                                    default=datetime.datetime.now)  # date schedule modified


# table to record 'goes' for each event schedule
# TODO add go for event
class EventGo(models.Model):
    eventSchedule = models.ForeignKey(EventSchedule, editable=False)
    #event = models.ForeignKey(EventSchedule, editable=False) # for performance
    user = models.ForeignKey(Account, editable=False, related_name='goesOnEvents')
    created = models.DateTimeField(auto_now_add=True)  # go created

    class Meta:
        unique_together = ('eventSchedule', 'user')

    @staticmethod
    def getGoesStatement(user):
        if not user or user.is_anonymous(): return 0
        goes = "SELECT 1 FROM dual WHERE EXISTS ( SELECT id FROM %s WHERE %s=%d and %s=SCH.`id` LIMIT 1)" % \
               ( EventGo._meta.db_table,
                 EventGo.user.field.column,
                 user.pk,
                 EventGo.eventSchedule.field.column)
        return goes


# event comments
class Comment(models.Model):
    COMMENT_TYPE = (
        (u'P', u'positive'),
        (u'N', u'negative'),
        (u'U', u'neutral')
    )
    event = models.ForeignKey(Event)
    author = models.ForeignKey(Account)
    type = models.CharField(max_length=1, choices=COMMENT_TYPE, default='U')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True) #created


class Invite(models.Model):
    """

    """
    event = models.ForeignKey(Event)
    user = models.ForeignKey(Account, related_name='invites')
    person = models.ForeignKey(Account, related_name='invited')
    created = models.DateTimeField(auto_now_add=True) #created

    class Meta:
        unique_together = ('event', 'user', 'person')

