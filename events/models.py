from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from blogs.models import Blog

class Event(models.Model):
    name = models.CharField(max_length=255)
    blogId = models.ForeignKey(Blog) #indicates to which blog this event belongs
    #TODO placeId = models.OneToOneField(Place) #place where event holds
    descr = models.TextField() #event description (br code)
    rating = models.FloatField() #event rating
    type = models.PositiveIntegerField() #bitmask of event types
    category = models.IntegerField() #bitmask of categories where this event must be shown
    dateFrom = models.DateTimeField() #date when event starts
    dateTo = models.DateTimeField() #date when event ends
    created = models.DateTimeField(auto_now_add=True) #date event created
    participants = models.PositiveIntegerField() # number of participants


class Invite(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User, related_name='invites')
    person = models.ForeignKey(User, related_name='invited')
