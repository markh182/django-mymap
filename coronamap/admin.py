from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Covid19Info, LeafletGeoAdmin)
