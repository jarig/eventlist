from django.contrib.auth.models import User
from django.db import models


class Types(models.Model):
    name = models.CharField(max_length=64)
    icon = models.ImageField(upload_to="blog/type_icon/", default=None)
    confirmed = models.BooleanField()
    
    def __unicode__(self):
        return self.name

class BlogStyle(models.Model):
    TYPE = (
        (u'F',u'free'),
        (u'P',u'premium'),
    )
    name = models.CharField(max_length=64)
    default = models.BooleanField(default=False)
    type = models.CharField(max_length=1,choices=TYPE)

    def __unicode__(self):
        return self.name

# Create your models here.
class Blog(models.Model):
    BLOG_TYPE =(
        (u'RR',u'regular'),
        (u'GD',u'business')
    )
    managers = models.ManyToManyField(User, through='BlogAccess') #indicates which users has access to blog
    name = models.CharField(max_length=64)
    description = models.TextField(default="")
    logo = models.ImageField(upload_to="blog/logo/",)
    type = models.CharField(max_length=2, choices=BLOG_TYPE, default='RR') #type of the blog
    priority = models.PositiveIntegerField(default=0) #priorty of blog during search
    rating = models.PositiveIntegerField(default=0) #blogs rating
    style = models.ForeignKey(BlogStyle, default=1)
    types = models.ManyToManyField(Types)

#which users has access to this blog
class BlogAccess(models.Model):
    ACCESS_TYPE = (
        (u'OW',u'owner'),
        (u'AD',u'admin'),
        (u'MN',u'manager'),
        (u'PB',u'publisher'),
    )
    blog = models.ForeignKey(Blog)
    user = models.ForeignKey(User)
    access = models.CharField(max_length=2, choices=ACCESS_TYPE)

