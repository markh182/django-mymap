from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView
from .models import Covid19Info, Covid19InfoByCountry
from django.db.models import Sum
import datetime

today = datetime.date.today()
yesterday = today - datetime.timedelta(days = 1)

# Create your views here.
class CovidMap(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):

        try:
            object = Covid19Info.objects.last()
        except Covid19Info.DoesNotExist:
            object = None
        if object:
            last_date = Covid19Info.objects.latest('date')
            date = last_date.date
        else:
            date = today

        last_date = Covid19Info.objects.latest('date')
        context = super(CovidMap, self).get_context_data(**kwargs)
        context['confirmed'] = Covid19Info.objects.order_by('-confirmed').filter(date=date)
        context['confirmed_number'] = Covid19Info.objects.filter(date=date).aggregate(Sum('confirmed'))
        context['deaths'] = Covid19Info.objects.order_by('-deaths').filter(date=date)
        context['deaths_number'] = Covid19Info.objects.filter(date=date).aggregate(Sum('deaths'))
        context['recovered'] = Covid19Info.objects.order_by('-recovered').filter(date=date)
        context['recovered_number'] = Covid19Info.objects.filter(date=date).aggregate(Sum('recovered'))
        return context

class CovidMapByCountry(TemplateView):
    template_name = "indexbycountry.html"

    def get_context_data(self, **kwargs):

        try:
            object = Covid19InfoByCountry.objects.last()
        except Covid19InfoByCountry.DoesNotExist:
            object = None
        if object:
            last_date = Covid19InfoByCountry.objects.latest('date')
            date = last_date.date
        else:
            date = today

        context = super(CovidMapByCountry, self).get_context_data(**kwargs)
        context['confirmed'] = Covid19InfoByCountry.objects.order_by('-confirmed').filter(date=date).filter(country=self.kwargs.get('country'))
        context['confirmed_number'] = Covid19InfoByCountry.objects.filter(date=date).filter(country=self.kwargs.get('country')).aggregate(Sum('confirmed'))
        context['deaths'] = Covid19InfoByCountry.objects.order_by('-deaths').filter(date=date).filter(country=self.kwargs.get('country'))
        context['deaths_number'] = Covid19InfoByCountry.objects.filter(date=date).filter(country=self.kwargs.get('country')).aggregate(Sum('deaths'))
        context['diff'] = Covid19InfoByCountry.objects.order_by('-difference').filter(date=date).filter(country=self.kwargs.get('country'))
        context['diff_number'] = Covid19InfoByCountry.objects.filter(date=date).filter(country=self.kwargs.get('country')).aggregate(Sum('difference'))
        context['centralCountry'] =  Covid19Info.objects.all().filter(country=self.kwargs.get('country')).filter(province='')[:1]
        context['country'] = self.kwargs.get('country')
        return context

class CovidMapByProvince(TemplateView):
    template_name = "indexbyprovince.html"

    def get_context_data(self, **kwargs):

        try:
            object = Covid19InfoByCountry.objects.last()
        except Covid19InfoByCountry.DoesNotExist:
            object = None
        if object:
            last_date = Covid19InfoByCountry.objects.latest('date')
            date = last_date.date
        else:
            date = today

        context = super(CovidMapByProvince, self).get_context_data(**kwargs)
        context['confirmed'] = Covid19InfoByCountry.objects.order_by('-confirmed').filter(date=date).filter(country=self.kwargs.get('country')).filter(province=self.kwargs.get('province'))
        context['confirmed_number'] = Covid19InfoByCountry.objects.filter(date=date).filter(country=self.kwargs.get('country')).filter(province=self.kwargs.get('province')).aggregate(Sum('confirmed'))
        context['deaths'] = Covid19InfoByCountry.objects.order_by('-deaths').filter(date=date).filter(country=self.kwargs.get('country')).filter(province=self.kwargs.get('province'))
        context['deaths_number'] = Covid19InfoByCountry.objects.filter(date=date).filter(country=self.kwargs.get('country')).filter(province=self.kwargs.get('province')).aggregate(Sum('deaths'))
        context['diff'] = Covid19InfoByCountry.objects.order_by('-difference').filter(date=date).filter(country=self.kwargs.get('country')).filter(province=self.kwargs.get('province'))
        context['diff_number'] = Covid19InfoByCountry.objects.filter(date=date).filter(country=self.kwargs.get('country')).filter(province=self.kwargs.get('province')).aggregate(Sum('difference'))
        context['centralCountry'] =  Covid19InfoByCountry.objects.all().filter(country=self.kwargs.get('country')).filter(province=self.kwargs.get('province'))[:1]
        context['country'] = self.kwargs.get('country')
        context['province'] = self.kwargs.get('province')
        return context


class MapLayer(GeoJSONLayerView):
    model = Covid19Info
    properties=('combinedKey', 'confirmed', 'deaths', 'recovered', 'active', 'province') # properties : list of properties names, or dict for mapping field names and properties
    simplify = 0.5 # simplify : generalization of geometries (See simplify())
    precision = 4 # precision : number of digit after comma
    geometry_field = 'geom' # geometry_field : name of geometry field (default: geom)
    srid = 4326 # srid : projection (default: 4326, for WGS84)
    # bbox : Allows you to set your own bounding box on feature collection level
    bbox_auto = False # bbox_auto : True/False (default false). Will automatically generate a bounding box on a per feature level.
    use_natural_keys = False # use_natural_keys : serialize natural keys instead of primary keys (default: False)

    def get_queryset(self):

        try:
            object = Covid19Info.objects.last()
        except Covid19Info.DoesNotExist:
            object = None
        if object:
            last_date = Covid19Info.objects.latest('date')
            date = last_date.date
        else:
            date = today

        queryset = Covid19Info.objects.filter(date=date)
        return queryset

class MapLayerByCountry(GeoJSONLayerView):
    model = Covid19InfoByCountry
    properties=('combinedKey', 'confirmed', 'deaths', 'difference', 'province', 'difference') # properties : list of properties names, or dict for mapping field names and properties
    simplify = 0.5 # simplify : generalization of geometries (See simplify())
    precision = 4 # precision : number of digit after comma
    geometry_field = 'geom' # geometry_field : name of geometry field (default: geom)
    srid = 4326 # srid : projection (default: 4326, for WGS84)
    # bbox : Allows you to set your own bounding box on feature collection level
    bbox_auto = False # bbox_auto : True/False (default false). Will automatically generate a bounding box on a per feature level.
    use_natural_keys = False # use_natural_keys : serialize natural keys instead of primary keys (default: False)

    def get_queryset(self):

        try:
            object = Covid19InfoByCountry.objects.last()
        except Covid19InfoByCountry.DoesNotExist:
            object = None
        if object:
            last_date = Covid19InfoByCountry.objects.latest('date')
            date = last_date.date
        else:
            date = today

        queryset = Covid19InfoByCountry.objects.filter(country=self.kwargs.get('country')).filter(date=date)
        return queryset

class MapLayerByProvince(GeoJSONLayerView):
    model = Covid19InfoByCountry
    properties=('combinedKey', 'confirmed', 'deaths', 'difference', 'province', 'difference') # properties : list of properties names, or dict for mapping field names and properties
    simplify = 0.5 # simplify : generalization of geometries (See simplify())
    precision = 4 # precision : number of digit after comma
    geometry_field = 'geom' # geometry_field : name of geometry field (default: geom)
    srid = 4326 # srid : projection (default: 4326, for WGS84)
    # bbox : Allows you to set your own bounding box on feature collection level
    bbox_auto = False # bbox_auto : True/False (default false). Will automatically generate a bounding box on a per feature level.
    use_natural_keys = False # use_natural_keys : serialize natural keys instead of primary keys (default: False)

    def get_queryset(self):

        try:
            object = Covid19InfoByCountry.objects.last()
        except Covid19InfoByCountry.DoesNotExist:
            object = None
        if object:
            last_date = Covid19InfoByCountry.objects.latest('date')
            date = last_date.date
        else:
            date = today

        queryset = Covid19InfoByCountry.objects.filter(country=self.kwargs.get('country')).filter(province=self.kwargs.get('province')).filter(date=date)
        return queryset
