from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=128)

class Address(models.Model):
    name = models.CharField(max_length=255, default='') #location name
    country = models.ForeignKey(Country)
    cityArea = models.CharField(max_length=128, default='') #
    city = models.CharField(max_length=128)
    county = models.CharField(max_length=128, default='')
    street = models.CharField(max_length=255)
    postalCode = models.CharField(max_length=15, default='')

    
