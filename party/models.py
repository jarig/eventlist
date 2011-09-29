from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Party(models.Model):
    ROLE = (
        (u'O',u'organizer'),
        (u'P',u'participant'),
    )
    participant = models.ManyToManyField(User, through='Participation')
    role = models.CharField(max_length=1, choices=ROLE, default='P')
    
    pass #party model


class Participation(models.Model):

    party = models.ForeignKey(Party)
    user = models.ForeignKey(User)
    
    dateAdded = models.DateTimeField(auto_now_add=True)
    
    pass