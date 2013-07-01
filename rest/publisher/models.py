from django.db import models

# Create your models here.
from account.models import Account

class PublisherRequest(models.Model):

    class STATUS:
        REQUESTED = u"R"
        ACCEPTED = u"A"
        DECLINED = u"D"
    STATUSES= (
        (STATUS.REQUESTED,u'requested'),
        (STATUS.ACCEPTED,u'accepted'),
        (STATUS.DECLINED,u'declined'),
    )
    user = models.OneToOneField(Account)
    message = models.TextField()
    status = models.CharField(choices=STATUSES, default=STATUS.REQUESTED, max_length=1)
    dateAdded = models.DateTimeField(auto_now_add=True) #date event created

    #create permissions
    class Meta:
        permissions = (
            ("publish", "Can publish events in blogs"),
        )
    