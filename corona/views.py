from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView
from .models import Covid19, Borders
from django.db.models import Sum
import datetime

today = datetime.date.today()
# yesterday = today - datetime.timedelta(days = 1)

# Create your views here.
class WorldMap(TemplateView):
    template_name = "world.html"

    def get_context_data(self, **kwargs):
        level = "country"

        try:
            object = Covid19.objects.last()
        except Covid19.DoesNotExist:
            object = None
        if object:
            last_date = Covid19.objects.latest('date')
            date = last_date.date
        else:
            date = today

        data = Covid19.objects.order_by('-confirmed').filter(date=date).filter(level=level)
        context = super(WorldMap, self).get_context_data(**kwargs)

        if data:
            context['data'] = data
            context['confirmed_number'] = Covid19.objects.filter(date=date).filter(level=level).aggregate(Sum('confirmed'))
            context['deaths_number'] = Covid19.objects.filter(date=date).filter(level=level).aggregate(Sum('deaths'))
            context['recovered_number'] = Covid19.objects.filter(date=date).filter(level=level).aggregate(Sum('recovered'))
            context['difference_number'] = Covid19.objects.filter(date=date).filter(level=level).aggregate(Sum('difference'))
            context['date'] = data.latest('date')
        else :
            context['data'] = ''
            context['confirmed_number'] = 0
            context['deaths_number'] = 0
            context['recovered_number'] = 0
            context['difference_number'] = 0
            context['date'] = date

        return context

class WorldMapLayer(GeoJSONLayerView):
    properties=('country_name', 'state', 'county', 'confirmed', 'deaths', 'recovered', 'difference') # properties : list of properties names, or dict for mapping field names and properties
    simplify = 0.5 # simplify : generalization of geometries (See simplify())
    precision = 4 # precision : number of digit after comma
    geometry_field = 'geom' # geometry_field : name of geometry field (default: geom)
    srid = 4326 # srid : projection (default: 4326, for WGS84)
    # bbox : Allows you to set your own bounding box on feature collection level
    bbox_auto = False # bbox_auto : True/False (default false). Will automatically generate a bounding box on a per feature level.
    use_natural_keys = False # use_natural_keys : serialize natural keys instead of primary keys (default: False)

    def get_queryset(self):
        level = "country"

        try:
            object = Covid19.objects.last()
        except Covid19.DoesNotExist:
            object = None
        if object:
            last_date = Covid19.objects.latest('date')
            date = last_date.date
        else:
            date = today

        queryset = Covid19.objects.filter(date=date).filter(level=level)
        return queryset

class CountryMap(TemplateView):
    template_name = "country.html"

    def get_context_data(self, **kwargs):
        level = "state"
        country = self.kwargs.get('country')

        try:
            object = Covid19.objects.last()
        except Covid19.DoesNotExist:
            object = None
        if object:
            last_date = Covid19.objects.latest('date')
            date = last_date.date
        else:
            date = today

        data = Covid19.objects.order_by('-confirmed').filter(date=date).filter(level=level).filter(country_slug=country)

        context = super(CountryMap, self).get_context_data(**kwargs)

        if data:
            context['data'] = data
            context['confirmed_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).aggregate(Sum('confirmed'))
            context['deaths_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).aggregate(Sum('deaths'))
            context['recovered_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).aggregate(Sum('recovered'))
            context['difference_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).aggregate(Sum('difference'))
            context['centralCountry'] =  Covid19.objects.all().filter(country_slug=country).filter(level='country').filter(state='').filter(county='')[:1]
            context['country'] = country
            context['date'] = date
            context['country_name'] = data[0].country_name
        else :
            context['data'] = ''
            context['confirmed_number'] = Covid19.objects.filter(date=date).filter(level='country').filter(country_slug=country).aggregate(Sum('confirmed'))
            context['deaths_number'] = Covid19.objects.filter(date=date).filter(level='country').filter(country_slug=country).aggregate(Sum('deaths'))
            context['recovered_number'] = Covid19.objects.filter(date=date).filter(level='country').filter(country_slug=country).aggregate(Sum('recovered'))
            context['difference_number'] = Covid19.objects.filter(date=date).filter(level='country').filter(country_slug=country).aggregate(Sum('difference'))
            context['centralCountry'] =  Covid19.objects.all().filter(country_slug=country).filter(level='country').filter(state='').filter(county='')[:1]
            context['country'] = country
            context['date'] = date
            context['country_name'] = country

        return context

class CountryMapLayer(GeoJSONLayerView):
    properties=('country_name', 'state', 'county', 'confirmed', 'deaths', 'recovered', 'difference') # properties : list of properties names, or dict for mapping field names and properties
    simplify = 0.5 # simplify : generalization of geometries (See simplify())
    precision = 4 # precision : number of digit after comma
    geometry_field = 'geom' # geometry_field : name of geometry field (default: geom)
    srid = 4326 # srid : projection (default: 4326, for WGS84)
    # bbox : Allows you to set your own bounding box on feature collection level
    bbox_auto = False # bbox_auto : True/False (default false). Will automatically generate a bounding box on a per feature level.
    use_natural_keys = False # use_natural_keys : serialize natural keys instead of primary keys (default: False)

    def get_queryset(self):
        level = "state"
        country = self.kwargs.get('country')

        try:
            object = Covid19.objects.last()
        except Covid19.DoesNotExist:
            object = None
        if object:
            last_date = Covid19.objects.latest('date')
            date = last_date.date
        else:
            date = today

        queryset = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country)

        if not queryset:
            queryset = Covid19.objects.filter(date=date).filter(level='country').filter(country_slug=country)
        return queryset


class StateMap(TemplateView):
    template_name = "state.html"

    def get_context_data(self, **kwargs):
        level = "county"
        country = self.kwargs.get('country')
        state = self.kwargs.get('state')

        try:
            object = Covid19.objects.last()
        except Covid19.DoesNotExist:
            object = None
        if object:
            last_date = Covid19.objects.filter(level='county').filter(country_slug=country).filter(state_slug=state).latest('date')
            date = last_date.date
        else:
            date = today

        data = Covid19.objects.order_by('-confirmed').filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state)
        context = super(StateMap, self).get_context_data(**kwargs)

        if data:
            context['data'] = data
            context['confirmed_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state).aggregate(Sum('confirmed'))
            context['deaths_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state).aggregate(Sum('deaths'))
            context['recovered_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state).aggregate(Sum('recovered'))
            context['difference_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state).aggregate(Sum('difference'))
            context['centralCountry'] =  Covid19.objects.all().filter(country_slug=country).filter(level='state').filter(state_slug=state).filter(county='')[:1]
            context['country'] = country
            context['state'] = state
            context['date'] = date
            context['state_name'] = data[0].state
        else :
            level = "state"
            context['confirmed_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state).aggregate(Sum('confirmed'))
            context['deaths_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state).aggregate(Sum('deaths'))
            context['recovered_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state).aggregate(Sum('recovered'))
            context['difference_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state).aggregate(Sum('difference'))
            context['centralCountry'] =  Covid19.objects.all().filter(country_slug=country).filter(level='state').filter(state_slug=state).filter(county='')[:1]
            context['country'] = country
            context['state'] = state
            context['date'] = date
            context['state_name'] = state

        if country == 'Germany' or country == 'germany':
            if data:
                borders = Borders.objects.filter(country=country).filter(state=state)
            else:
                borders = Borders.objects.filter(level='state').filter(country=country).filter(state=state)
            context['borders'] = borders

        return context

class StateMapLayer(GeoJSONLayerView):
    properties=('country_name', 'state', 'county', 'confirmed', 'deaths', 'recovered', 'difference') # properties : list of properties names, or dict for mapping field names and properties
    simplify = 0.5 # simplify : generalization of geometries (See simplify())
    precision = 4 # precision : number of digit after comma
    geometry_field = 'geom' # geometry_field : name of geometry field (default: geom)
    srid = 4326 # srid : projection (default: 4326, for WGS84)
    # bbox : Allows you to set your own bounding box on feature collection level
    bbox_auto = False # bbox_auto : True/False (default false). Will automatically generate a bounding box on a per feature level.
    use_natural_keys = False # use_natural_keys : serialize natural keys instead of primary keys (default: False)

    def get_queryset(self):
        level = "county"
        country = self.kwargs.get('country')
        state = self.kwargs.get('state')

        try:
            object = Covid19.objects.last()
        except Covid19.DoesNotExist:
            object = None
        if object:
            last_date = Covid19.objects.filter(level='county').filter(country_slug=country).filter(state_slug=state).latest('date')
            date = last_date.date
        else:
            date = today

        queryset = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state)

        if not queryset:
            queryset = Covid19.objects.filter(date=date).filter(level='state').filter(country_slug=country).filter(state_slug=state)
        return queryset

class CountyMap(TemplateView):
    template_name = "county.html"

    def get_context_data(self, **kwargs):
        level = "county"
        country = self.kwargs.get('country')
        state = self.kwargs.get('state')
        county = self.kwargs.get('county')

        try:
            object = Covid19.objects.last()
        except Covid19.DoesNotExist:
            object = None
        if object:
            last_date = Covid19.objects.filter(level='county').filter(country_slug=country).filter(state_slug=state).filter(county_slug=county).latest('date')
            date = last_date.date
        else:
            date = today

        data = Covid19.objects.order_by('-confirmed').filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state).filter(county_slug=county)
        context = super(CountyMap, self).get_context_data(**kwargs)

        if data:
            context['data'] = data
            context['confirmed_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state).filter(county_slug=county).aggregate(Sum('confirmed'))
            context['deaths_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state).filter(county_slug=county).aggregate(Sum('deaths'))
            context['recovered_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state).filter(county_slug=county).aggregate(Sum('recovered'))
            context['difference_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state).filter(county_slug=county).aggregate(Sum('difference'))
            context['centralCountry'] =  Covid19.objects.all().filter(country_slug=country).filter(level='county').filter(state_slug=state).filter(county_slug=county)[:1]
            context['country'] = country
            context['state'] = state
            context['county'] = county
            context['date'] = date
            context['county_name'] = data[0].county
        else :
            level = "county"
            context['confirmed_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state).aggregate(Sum('confirmed'))
            context['deaths_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state).aggregate(Sum('deaths'))
            context['recovered_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state).aggregate(Sum('recovered'))
            context['difference_number'] = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state).aggregate(Sum('difference'))
            context['centralCountry'] =  Covid19.objects.all().filter(country_slug=country).filter(level='county').filter(state_slug=state).filter(county_slug=county)[:1]
            context['country'] = country
            context['state'] = state
            context['date'] = date
            context['county_name'] = county

        if country == 'Germany' or country == 'germany':
            if data:
                borders = Borders.objects.filter(country=country).filter(state=state).filter(county=county)
            else:
                borders = Borders.objects.filter(level='county').filter(country=country).filter(state=state)
            context['borders'] = borders

        return context

class CountyMapLayer(GeoJSONLayerView):
    properties=('country_name', 'state', 'county', 'confirmed', 'deaths', 'recovered', 'difference') # properties : list of properties names, or dict for mapping field names and properties
    simplify = 0.5 # simplify : generalization of geometries (See simplify())
    precision = 4 # precision : number of digit after comma
    geometry_field = 'geom' # geometry_field : name of geometry field (default: geom)
    srid = 4326 # srid : projection (default: 4326, for WGS84)
    # bbox : Allows you to set your own bounding box on feature collection level
    bbox_auto = False # bbox_auto : True/False (default false). Will automatically generate a bounding box on a per feature level.
    use_natural_keys = False # use_natural_keys : serialize natural keys instead of primary keys (default: False)

    def get_queryset(self):
        level = "county"
        country = self.kwargs.get('country')
        state = self.kwargs.get('state')
        county = self.kwargs.get('county')

        try:
            object = Covid19.objects.last()
        except Covid19.DoesNotExist:
            object = None
        if object:
            last_date = Covid19.objects.filter(level='county').filter(country_slug=country).filter(state_slug=state).filter(county_slug=county).latest('date')
            date = last_date.date
        else:
            date = today

        queryset = Covid19.objects.filter(date=date).filter(level=level).filter(country_slug=country).filter(state_slug=state).filter(county_slug=county)
        return queryset
