from datetime import datetime
from django.db import models
from blog.models import Blog


class Album(models.Model):
    blog = models.ForeignKey(Blog)
    description = models.TextField(default='')
    created = models.DateTimeField(auto_now_add=True, default=datetime.now())


class Image(models.Model):
    album = models.ForeignKey(Album)
    url = models.ImageField(upload_to='/album/image/') #url to image
    caption = models.CharField(max_length=64)
    added = models.DateTimeField(auto_now=True, default=datetime.now())
    
