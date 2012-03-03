import datetime
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Message(models.Model):
    class STATUS:
        SENT = 0
        RECEIVED  = 1
        DELETED_AUTHOR = 2
        DELETED_CORRESPONDENT = 4
    _STATUS = (
        (STATUS.SENT, u'sent'),
        (STATUS.RECEIVED, u'received'),
        (STATUS.DELETED_AUTHOR, u'deleted by author'),
        (STATUS.DELETED_CORRESPONDENT, u'deleted by correspondent'),
    )
    subject = models.CharField(max_length=255, default='')
    text = models.TextField()
    author = models.ForeignKey(User, related_name='sent_messages')
    to = models.ForeignKey(User, related_name='received_messages')
    # 0 - sent, 1 - received, 2 - deleted by author, 4 - deleted by correspondent
    status = models.PositiveSmallIntegerField(editable=False, default=0)
    sent = models.DateTimeField(auto_now_add=True, auto_now=True, default=datetime.date.today)


