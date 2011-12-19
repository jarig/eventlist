import datetime
from django.contrib.auth.models import User
from django.db import models
from blogs.models import Blog
from common.models import Address
from organization.models import Organization


class EventActivity(models.Model):
    name = models.CharField(max_length=128)
    icon = models.ImageField(upload_to="event/event_type/icon/", blank=True, default='')
    thumbnail = models.ImageField(upload_to="event/event_type/thumb/", blank=True, default='')
    confirmed = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name
    class Meta:
        unique_together = ('name',)

class Event(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User)
    logo = models.ImageField(upload_to="event/logo/",)
    blogs = models.ManyToManyField(Blog) #indicates
    activities = models.ManyToManyField(EventActivity, blank=True, null=True) #event activities/actions
    organizers = models.ManyToManyField(Organization)
    descr = models.TextField() #event description (BB code)
    rating = models.FloatField(default=0) #event rating
    created = models.DateTimeField(auto_now_add=True) #date event created
    participants = models.PositiveIntegerField(default=0) # number of participants, help num (not exact)
    confirmed = models.BooleanField(editable=False, default=True) #event confirmed by blog/page admins
    
# Event may have many schedules
class EventSchedule(models.Model):
    event = models.ForeignKey(Event, editable=False)
    dateFrom = models.DateField(default=datetime.date.today) #date when event starts
    timeFrom = models.TimeField(default='00:00')
    dateTo = models.DateField(null=True, blank=True, default=datetime.date.today) #date when event ends
    timeTo = models.TimeField(default='00:00', null=True, blank=True)
    address = models.ForeignKey(Address, null=True) #location where this event will be held
    blog = models.ForeignKey(Blog, null=True, blank=True, default='') # addresses's blog
    
    pass

class Comment(models.Model):
    COMMENT_TYPE = (
        (u'P',u'positive'),
        (u'N',u'negative'),
        (u'U',u'neutral')
    )
    event = models.ForeignKey(Event)
    author = models.ForeignKey(User)
    type = models.CharField(max_length=1, choices=COMMENT_TYPE, default='U')
    text = models.TextField()
    

class Invite(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User, related_name='invites')
    person = models.ForeignKey(User, related_name='invited')

    class Meta:
        unique_together = ('event', 'user', 'person')
