from django.db import models

# Create your models here.
from common.managers import AddressManager


class Country(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=128)
    rating = models.PositiveIntegerField(default=0)

    def natural_key(self):
        return self.name

    def __unicode__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=128)
    confirmed = models.BooleanField(default=False, editable=False)
    
    def natural_key(self):
        return self.name

    def __unicode__(self):
        return self.name

class Address(models.Model):
    name = models.CharField(max_length=255, default='', blank=True) #location name
    country = models.ForeignKey(Country)
    city = models.ForeignKey(City)
    cityArea = models.CharField(max_length=128, default='', blank=True)
    county = models.CharField(max_length=128, default='', blank=True)
    street = models.CharField(max_length=255)
    postalCode = models.CharField(max_length=15, default='', blank=True)
    token = models.CharField(max_length=32, default=None, null=True, editable=False)

    objects = AddressManager()

    def __init__(self, *args, **kwargs):
        super(Address, self).__init__(*args, **kwargs)

    def natural_key(self):
        return self.name

    def __unicode__(self):
        return "%s, %s, %s, %s" % (self.name, self.street, self.country, self.city)

class Language(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=64)

    def natural_key(self):
        return self.name

    def __unicode__(self):
        return self.name