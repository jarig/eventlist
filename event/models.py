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
    blogs = models.ManyToManyField(Blog) #indicates to which blogs this event belongs to
    activities = models.ManyToManyField(EventActivity, blank=True, null=True)
    addresses = models.ManyToManyField(Address, blank=True, null=True) #locations where this event will be held
    organizers = models.ManyToManyField(Organization)
    descr = models.TextField() #event description (BB code)
    rating = models.FloatField(default=0) #event rating
    dateFrom = models.DateField() #date when event starts
    timeFrom = models.TimeField(default='00:00')
    dateTo = models.DateField() #date when event ends
    timeTo = models.TimeField(default='00:00')
    created = models.DateTimeField(auto_now_add=True) #date event created
    participants = models.PositiveIntegerField(default=0) # number of participants


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
