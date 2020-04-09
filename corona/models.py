from djgeojson.fields import PointField, PolygonField
from django.db import models

# Create your models here.
class Borders(models.Model):
    level = models.CharField(max_length=64, default='')
    country = models.CharField(max_length=64, default='')
    state = models.CharField(max_length=64, blank=True, null=True, default='')
    county = models.CharField(max_length=255, blank=True, null=True, default='')
    # geom = PointField(default='{}')
    polygon = PolygonField(default='{}')
    # long = models.CharField(max_length=30, default=0)
    # lat = models.CharField(max_length=30, default=0)
    # def __str__(self):
    #     return (self.name+', '+self.short_name)


class Covid19(models.Model):

    date = models.DateTimeField(null=True)
    level = models.CharField(max_length=64, default='')
    country_name = models.CharField(max_length=64, default='')
    country_key = models.CharField(max_length=64, default='')
    country_slug = models.SlugField(max_length=64, default='')
    state = models.CharField(max_length=64, blank=True, null=True, default='')
    state_slug = models.CharField(max_length=64, blank=True, null=True, default='')
    county = models.CharField(max_length=255, blank=True, null=True, default='')
    county_slug = models.CharField(max_length=255, blank=True, null=True, default='')
    population = models.PositiveIntegerField(default=0)
    geom = PointField(default='{}')
    polygon = PolygonField(default='{}')
    long = models.CharField(max_length=30, default=0)
    lat = models.CharField(max_length=30, default=0)
    confirmed = models.PositiveIntegerField(default=0)
    confirmed_difference = models.IntegerField(default=0)
    deaths = models.PositiveIntegerField(default=0)
    deaths_difference = models.IntegerField(default=0)
    recovered = models.PositiveIntegerField(default=0)
    recovered_difference = models.IntegerField(default=0)
    tested = models.PositiveIntegerField(default=0)
    tested_difference = models.IntegerField(default=0)
    jsonkey = models.CharField(max_length=255, null=True)

    def __str__(self):
        return (self.jsonkey)+' '+str(self.date)
