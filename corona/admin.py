from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from . import models

# Register your models here.
# admin.site.register(models.Country, LeafletGeoAdmin)
# admin.site.register(models.State, LeafletGeoAdmin)
admin.site.register(models.Borders, LeafletGeoAdmin)
admin.site.register(models.Covid19, LeafletGeoAdmin)
