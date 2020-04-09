from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView
from .models import Covid19, Borders
from django.db.models import Sum
import datetime

today = datetime.date.today()
yesterday = today - datetime.timedelta(days = 1)

# Create your views here.
class WorldMap(TemplateView):
    template_name = "world.html"

    def get_context_data(self, **kwargs):
        level = "country"

        object = Covid19.objects.last()
        if object:
            date = Covid19.objects.filter(level=level).latest('date').date
        else:
            date = today

        data = Covid19.objects.filter(level=level).filter(date=date)

        context = super(WorldMap, self).get_context_data(**kwargs)
        if data:
            context['data'] = data.order_by('-confirmed')
            context['confirmed_sum'] = data.aggregate(Sum('confirmed'))
            context['deaths_sum'] = data.aggregate(Sum('deaths'))
            context['recovered_sum'] = data.aggregate(Sum('recovered'))
            context['tested_sum'] = data.aggregate(Sum('tested'))
            context['confirmed_difference_sum'] = data.aggregate(Sum('confirmed_difference'))
            context['deaths_difference_sum'] = data.aggregate(Sum('deaths_difference'))
            context['recovered_difference_sum'] = data.aggregate(Sum('recovered_difference'))
            context['tested_difference_sum'] = data.aggregate(Sum('tested_difference'))
            context['date'] = data.latest('date')
        else :
            context['data'] = ''
            context['confirmed_sum'] = 0
            context['deaths_sum'] = 0
            context['recovered_sum'] = 0
            context['tested_sum'] = 0
            context['confirmed_difference_sum'] = 0
            context['deaths_difference_sum'] = 0
            context['recovered_difference_sum'] = 0
            context['tested_difference_sum'] = 0
            context['date'] = date

        borders = Borders.objects.filter(level=level).filter(state='').filter(county='')
        context['borders'] = borders

        return context


class WorldMapLayer(GeoJSONLayerView):
    properties=('country_name', 'state', 'county', 'confirmed', 'deaths', 'recovered', 'tested', 'confirmed_difference', 'deaths_difference', 'recovered_difference', 'tested_difference') # properties : list of properties names, or dict for mapping field names and properties
    simplify = 0.5 # simplify : generalization of geometries (See simplify())
    precision = 4 # precision : number of digit after comma
    geometry_field = 'geom' # geometry_field : name of geometry field (default: geom)
    srid = 4326 # srid : projection (default: 4326, for WGS84)
    # bbox : Allows you to set your own bounding box on feature collection level
    bbox_auto = False # bbox_auto : True/False (default false). Will automatically generate a bounding box on a per feature level.
    use_natural_keys = False # use_natural_keys : serialize natural keys instead of primary keys (default: False)

    def get_queryset(self):
        level = "country"

        object = Covid19.objects.last()
        if object:
            date = Covid19.objects.filter(level=level).latest('date').date
        else:
            date = today

        queryset = Covid19.objects.filter(level=level).filter(date=date)
        return queryset


class CountryMap(TemplateView):
    template_name = "country.html"

    def get_context_data(self, **kwargs):
        level = "state"
        country = self.kwargs.get('country')

        object = Covid19.objects.filter(level=level).filter(country_slug=country).last()
        if object:
            date = Covid19.objects.filter(level=level).filter(country_slug=country).latest('date').date
        else:
            date = today

        data = Covid19.objects.filter(level=level).filter(country_slug=country).filter(date=date)

        context = super(CountryMap, self).get_context_data(**kwargs)
        if data:
            context['data'] = data.order_by('-confirmed')
            context['confirmed_sum'] = data.aggregate(Sum('confirmed'))
            context['deaths_sum'] = data.aggregate(Sum('deaths'))
            context['recovered_sum'] = data.aggregate(Sum('recovered'))
            context['tested_sum'] = data.aggregate(Sum('tested'))
            context['confirmed_difference_sum'] = data.aggregate(Sum('confirmed_difference'))
            context['deaths_difference_sum'] = data.aggregate(Sum('deaths_difference'))
            context['recovered_difference_sum'] = data.aggregate(Sum('recovered_difference'))
            context['tested_difference_sum'] = data.aggregate(Sum('tested_difference'))
            context['centralCountry'] =  Covid19.objects.filter(level='country').filter(country_slug=country).filter(state='').filter(county='')[:1]
            context['country'] = country
            context['date'] = date
            context['country_name'] = data[0].country_name
        else :
            data = Covid19.objects.filter(level='country').filter(country_slug=country).filter(date__contains=date)
            context['data'] = ''
            context['confirmed_sum'] = data.aggregate(Sum('confirmed'))
            context['deaths_sum'] = data.aggregate(Sum('deaths'))
            context['recovered_sum'] = data.aggregate(Sum('recovered'))
            context['tested_sum'] = data.aggregate(Sum('tested'))
            context['confirmed_difference_sum'] = data.aggregate(Sum('confirmed_difference'))
            context['deaths_difference_sum'] = data.aggregate(Sum('deaths_difference'))
            context['recovered_difference_sum'] = data.aggregate(Sum('recovered_difference'))
            context['tested_difference_sum'] = data.aggregate(Sum('tested_difference'))
            context['centralCountry'] =  data.filter(state='').filter(county='')[:1]
            context['country'] = country
            context['date'] = date
            context['country_name'] = country

        if country == 'Germany' or country == 'germany':
            borders = Borders.objects.filter(level=level).filter(country=country).filter(county='')
            context['borders'] = borders
        else:
            borders = Borders.objects.filter(level='country').filter(country=country)
            context['borders'] = borders

        return context


class CountryMapLayer(GeoJSONLayerView):
    properties=('country_name', 'state', 'county', 'confirmed', 'deaths', 'recovered', 'tested', 'confirmed_difference', 'deaths_difference', 'recovered_difference', 'tested_difference') # properties : list of properties names, or dict for mapping field names and properties
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

        object = Covid19.objects.filter(level=level).filter(country_slug=country).last()
        if object:
            date = Covid19.objects.filter(level=level).filter(country_slug=country).latest('date').date
        else:
            date = today

        queryset = Covid19.objects.filter(level=level).filter(country_slug=country).filter(date=date)
        if not queryset:
            queryset = Covid19.objects.filter(level='country').filter(country_slug=country).filter(date__contains=date)
        return queryset


class StateMap(TemplateView):
    template_name = "state.html"

    def get_context_data(self, **kwargs):
        level = "county"
        country = self.kwargs.get('country')
        state = self.kwargs.get('state')

        object = Covid19.objects.filter(level=level).filter(country_slug=country).filter(state_slug=state).last()
        if object:
            date = Covid19.objects.filter(level=level).filter(country_slug=country).filter(state_slug=state).latest('date').date
        else:
            date = today

        data = Covid19.objects.filter(level=level).filter(country_slug=country).filter(state_slug=state).filter(date=date)

        context = super(StateMap, self).get_context_data(**kwargs)
        if data:
            context['data'] = data.order_by('-confirmed')
            context['confirmed_sum'] = data.aggregate(Sum('confirmed'))
            context['deaths_sum'] = data.aggregate(Sum('deaths'))
            context['recovered_sum'] = data.aggregate(Sum('recovered'))
            context['tested_sum'] = data.aggregate(Sum('tested'))
            context['confirmed_difference_sum'] = data.aggregate(Sum('confirmed_difference'))
            context['deaths_difference_sum'] = data.aggregate(Sum('deaths_difference'))
            context['recovered_difference_sum'] = data.aggregate(Sum('recovered_difference'))
            context['tested_difference_sum'] = data.aggregate(Sum('tested_difference'))
            context['centralCountry'] =  Covid19.objects.filter(level='state').filter(country_slug=country).filter(state_slug=state).filter(county='')[:1]
            context['country'] = country
            context['state'] = state
            context['date'] = date
            context['state_name'] = data[0].state
        else :
            data = Covid19.objects.filter(level='state').filter(country_slug=country).filter(state_slug=state).filter(date__contains=date)
            context['confirmed_sum'] = data.aggregate(Sum('confirmed'))
            context['deaths_sum'] = data.aggregate(Sum('deaths'))
            context['recovered_sum'] = data.aggregate(Sum('recovered'))
            context['tested_sum'] = data.aggregate(Sum('tested'))
            context['confirmed_difference_sum'] = data.aggregate(Sum('confirmed_difference'))
            context['deaths_difference_sum'] = data.aggregate(Sum('deaths_difference'))
            context['recovered_difference_sum'] = data.aggregate(Sum('recovered_difference'))
            context['tested_difference_sum'] = data.aggregate(Sum('tested_difference'))
            context['centralCountry'] =  data.filter(county='')[:1]
            context['country'] = country
            context['state'] = state
            context['date'] = date
            context['state_name'] = state

        if country == 'Germany' or country == 'germany':
            borders = Borders.objects.filter(level=level).filter(country=country).filter(state=state)
            context['borders'] = borders
        else:
            borders = Borders.objects.filter(level='country').filter(country=country)
            context['borders'] = borders

        return context

class StateMapLayer(GeoJSONLayerView):
    properties=('country_name', 'state', 'county', 'confirmed', 'deaths', 'recovered', 'tested', 'confirmed_difference', 'deaths_difference', 'recovered_difference', 'tested_difference') # properties : list of properties names, or dict for mapping field names and properties
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

        object = Covid19.objects.filter(level=level).filter(country_slug=country).filter(state_slug=state).last()
        if object:
            date = Covid19.objects.filter(level=level).filter(country_slug=country).filter(state_slug=state).latest('date').date
        else:
            date = today

        queryset = Covid19.objects.filter(level=level).filter(country_slug=country).filter(state_slug=state).filter(date=date)
        if not queryset:
            queryset = Covid19.objects.filter(level='state').filter(country_slug=country).filter(state_slug=state).filter(date__contains=date)
        return queryset

class CountyMap(TemplateView):
    template_name = "county.html"

    def get_context_data(self, **kwargs):
        level = "county"
        country = self.kwargs.get('country')
        state = self.kwargs.get('state')
        county = self.kwargs.get('county')

        object = Covid19.objects.filter(level=level).filter(country_slug=country).filter(state_slug=state).filter(county_slug=county).last()
        if object:
            date = Covid19.objects.filter(level=level).filter(country_slug=country).filter(state_slug=state).filter(county_slug=county).latest('date').date
        else:
            date = today

        data = Covid19.objects.filter(level=level).filter(country_slug=country).filter(state_slug=state).filter(county_slug=county).filter(date=date)

        context = super(CountyMap, self).get_context_data(**kwargs)
        if data:
            context['data'] = data.order_by('-confirmed')
            context['confirmed_sum'] = data.aggregate(Sum('confirmed'))
            context['deaths_sum'] = data.aggregate(Sum('deaths'))
            context['recovered_sum'] = data.aggregate(Sum('recovered'))
            context['tested_sum'] = data.aggregate(Sum('tested'))
            context['confirmed_difference_sum'] = data.aggregate(Sum('confirmed_difference'))
            context['deaths_difference_sum'] = data.aggregate(Sum('deaths_difference'))
            context['recovered_difference_sum'] = data.aggregate(Sum('recovered_difference'))
            context['tested_difference_sum'] = data.aggregate(Sum('tested_difference'))
            context['centralCountry'] =  Covid19.objects.filter(level='county').filter(country_slug=country).filter(state_slug=state).filter(county_slug=county)[:1]
            context['country'] = country
            context['state'] = state
            context['county'] = county
            context['date'] = date
            context['county_name'] = data[0].county
        else :
            data = Covid19.objects.filter(level='county').filter(country_slug=country).filter(state_slug=state).filter(date=date)
            context['confirmed_sum'] = data.aggregate(Sum('confirmed'))
            context['deaths_sum'] = data.aggregate(Sum('deaths'))
            context['recovered_sum'] = data.aggregate(Sum('recovered'))
            context['tested_sum'] = data.aggregate(Sum('tested'))
            context['confirmed_difference_sum'] = data.aggregate(Sum('confirmed_difference'))
            context['deaths_difference_sum'] = data.aggregate(Sum('deaths_difference'))
            context['recovered_difference_sum'] = data.aggregate(Sum('recovered_difference'))
            context['tested_difference_sum'] = data.aggregate(Sum('tested_difference'))
            context['centralCountry'] =  Covid19.objects.filter(level='county').filter(country_slug=country).filter(state_slug=state).filter(county_slug=county)[:1]
            context['country'] = country
            context['state'] = state
            context['date'] = date
            context['county_name'] = county

        if country == 'Germany' or country == 'germany':
            borders = Borders.objects.filter(level=level).filter(country=country).filter(state=state).filter(county=county)
            context['borders'] = borders
        else:
            borders = Borders.objects.filter(level='country').filter(country=country)
            context['borders'] = borders

        return context

class CountyMapLayer(GeoJSONLayerView):
    properties=('country_name', 'state', 'county', 'confirmed', 'deaths', 'recovered', 'tested', 'confirmed_difference', 'deaths_difference', 'recovered_difference', 'tested_difference') # properties : list of properties names, or dict for mapping field names and properties
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

        object = Covid19.objects.filter(level=level).filter(country_slug=country).filter(state_slug=state).filter(county_slug=county).last()
        if object:
            date = Covid19.objects.filter(level=level).filter(country_slug=country).filter(state_slug=state).filter(county_slug=county).latest('date').date
        else:
            date = today

        queryset = Covid19.objects.filter(level=level).filter(country_slug=country).filter(state_slug=state).filter(county_slug=county).filter(date=date)
        return queryset
