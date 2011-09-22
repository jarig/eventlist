from django.contrib.auth.models import User
from django.db import models


class Types(models.Model):
    name = models.CharField(max_length=64)
    #icon = models.ImageField(upload_to="blog/type/", default=None)
    #confirmed = models.BooleanField()
    
    def __unicode__(self):
        return self.name

# Create your models here.
class Blog(models.Model):
    BLOG_TYPE =(
        (u'PR',u'personal'),
        (u'BS',u'business')
    )
    managers = models.ManyToManyField(User, through='BlogAccess') #indicates which users has access to blog
    name = models.CharField(max_length=64)
    logo = models.ImageField(upload_to="blog/logo/",)
    type = models.CharField(max_length=2, choices=BLOG_TYPE) #type of the blog
    priority = models.PositiveIntegerField() #priorty of blog during search
    #style = models.CharField(max_length=64,default="default")#choosen blog style
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
