# Create your models here.
from djgeojson.fields import PointField
from django.db import models

class Covid19Info(models.Model):

    province = models.CharField(max_length=50, blank=True, null=True, default='')
    country = models.CharField(max_length=50, default='')
    date = models.DateField(null=True)
    lat = models.CharField(max_length=30, default=0)
    long = models.CharField(max_length=30, default=0)
    confirmed = models.PositiveIntegerField(default=0)
    deaths = models.PositiveIntegerField(default=0)
    recovered = models.PositiveIntegerField(default=0)
    active = models.PositiveIntegerField(default=0)
    combinedKey = models.CharField(max_length=50, null=True)
    geom = PointField(default='{}')

    def __str__(self):
        return self.country+' '+str(self.date)

class Covid19InfoByCountry(models.Model):

    province = models.CharField(max_length=50, blank=True, null=True, default='')
    country = models.CharField(max_length=50, default='')
    date = models.DateTimeField(null=True)
    lat = models.CharField(max_length=30, default=0)
    long = models.CharField(max_length=30, default=0)
    confirmed = models.PositiveIntegerField(default=0)
    deaths = models.PositiveIntegerField(default=0)
    recovered = models.PositiveIntegerField(default=0)
    active = models.PositiveIntegerField(default=0)
    difference = models.PositiveIntegerField(default=0)
    combinedKey = models.CharField(max_length=50, null=True)
    geom = PointField(default='{}')

    def __str__(self):
        return self.country+' '+str(self.date)
