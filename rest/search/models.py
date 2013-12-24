import datetime
import hashlib
from django.db import models


def defaultSearchTTL():
    return datetime.datetime.now() + datetime.timedelta(minutes=10)


class SearchRequest(models.Model):
    token = models.CharField(max_length=32, primary_key=True, editable=False)
    request = models.CharField(max_length=2048, editable=False)  # json formatted request
    name = models.CharField(max_length=128, default="", blank=True, verbose_name="Filter name")
    ttl = models.DateTimeField(null=True, blank=True, default=defaultSearchTTL,
                               help_text="Time to live", editable=False)

    def save(self, *args, **kwargs):
        self.token = hashlib.md5(self.request).hexdigest()
        super(SearchRequest, self).save(*args, **kwargs)