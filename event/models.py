from django.contrib.auth.models import User
from django.db import models
from blogs.models import Blog
from common.models import Address


class EventType(models.Model):
    name = models.CharField(max_length=128)


class Event(models.Model):
    name = models.CharField(max_length=255)
    blogId = models.ForeignKey(Blog) #indicates to which blog this event belongs to
    type = models.ManyToManyField(EventType)
    locations = models.ManyToManyField(Address, blank=True, null=True) #locations where this event will be held
    descr = models.TextField() #event description (BB code)
    rating = models.FloatField(default=0) #event rating
    dateFrom = models.DateTimeField() #date when event starts
    dateTo = models.DateTimeField() #date when event ends
    created = models.DateTimeField(auto_now_add=True) #date event created
    participants = models.PositiveIntegerField(default=0) # number of participants



class Invite(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User, related_name='invites')
    person = models.ForeignKey(User, related_name='invited')
