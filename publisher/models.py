from django.db import models

# Create your models here.
from account.models import Account

class PublisherRequest(models.Model):
    STATUSES= (
        (u'R',u'requested'),
        (u'A',u'accepted'),
        (u'D',u'declined'),
    )
    user = models.OneToOneField(Account)
    message = models.TextField()
    status = models.CharField(choices=STATUSES, default='R', max_length=1)
    dateAdded = models.DateTimeField(auto_now_add=True) #date event created

    #create permissions
    class Meta:
        permissions = (
            ("publish", "Can publish events in blogs"),
        )
    