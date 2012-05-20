from django.db import models
from account.models import Account
from _ext.pibu.fields import ImagePreviewModelField
from common.models import Address

class FacilityType(models.Model):
    #blog types ( bar/cafe/cinema )
    name = models.CharField(max_length=64)
    icon = models.ImageField(upload_to="blog/facility_type/icon/", default=None)
    thumbnail = models.ImageField(upload_to="blog/facility_type/thumb/", default=None)
    confirmed = models.BooleanField()

    class Meta:
        unique_together = ('name',)
    
    def __unicode__(self):
        return self.name

class BlogStyle(models.Model):
    STYLE_TYPE = (
        (u'F',u'free'),
        (u'P',u'premium'),
    )
    name = models.CharField(max_length=64)
    default = models.BooleanField(default=False)
    type = models.CharField(max_length=1,choices=STYLE_TYPE)

    def __unicode__(self):
        return self.name

def blog_logo_name(instance, filename):
    return "blog/logo/%d_main_logo" % int(instance.pk)


class Blog(models.Model):
    BLOG_TYPE =(
        (u'RR',u'regular'),
        (u'GD',u'gold')
    )
    managers = models.ManyToManyField(Account, through='BlogAccess') #indicates which users has access to blog
    name = models.CharField(max_length=64)
    description = models.TextField(default="")
    logo = ImagePreviewModelField(upload_to=blog_logo_name, max_width=150)
    type = models.CharField(max_length=2, choices=BLOG_TYPE, default='RR') #type of the blog
    priority = models.PositiveIntegerField(default=0) #priorty of blog during search
    rating = models.PositiveIntegerField(default=0) #blogs rating
    style = models.ForeignKey(BlogStyle, default=1)
    facilities = models.ManyToManyField(FacilityType, blank=True, null=True)
    addresses = models.ManyToManyField(Address, blank=True, null=True)
    
    def __unicode__(self):
        return self.name

#which users has access to this blog
class BlogAccess(models.Model):
    PUBLISHER = 15
    MANAGER = 30
    ADMIN = 45
    OWNER = 60
    ACCESS_LEVEL = (
        (PUBLISHER,u'PUBLISHER'), #can publish events, create news
        (MANAGER,u'MANAGER'), #publish events/accept requests
        (ADMIN,u'ADMIN'), #same priv. as owner, except deletion
        (OWNER,u'OWNER'),
    )
    accessLevelConstants = dict((x,y) for y,x in ACCESS_LEVEL)
    blog = models.ForeignKey(Blog)
    user = models.ForeignKey(Account)
    access = models.PositiveSmallIntegerField()
    class Meta:
        unique_together = ('blog','user','access',)



def getMaxPermission(blog, user):
        if blog is None or user is None: return -1
        bAccesses = blog.blogaccess_set.filter(user=user)
        maxIndex = -1 #has no permissions
        for bAccess in bAccesses:
            if bAccess.access > maxIndex:
                maxIndex = bAccess.access
        return maxIndex

