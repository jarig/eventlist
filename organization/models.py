from django.contrib.auth.models import User
from django.db import models
from common.models import Address

class Organization(models.Model):
    name = models.CharField(max_length=256)
    logo = models.ImageField(upload_to='organization/logo/')
    description = models.TextField(blank=True, default='')
    members = models.ManyToManyField(User, through='OrgAccess')
    address = models.ForeignKey(Address)
    
    phone = models.CharField(max_length=32)
    businessCode = models.CharField(max_length=16)
    pass

class OrgAccess(models.Model):
    ROLE1 = 10
    ROLE2 = 20
    OWNER = 30
    LEVELS = (
        (ROLE1,'ROLE1'),
        (ROLE2,'ROLE2'),
        (OWNER,'OWNER'),
    )
    member = models.ForeignKey(User)
    organization = models.ForeignKey(Organization)
    level = models.PositiveSmallIntegerField(choices=LEVELS)
    class Meta:
        unique_together = ('member','organization','level',)