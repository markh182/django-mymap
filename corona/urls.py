from django.urls import path
from . import views
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView
# from .models import Covid19
from .views import WorldMap, WorldMapLayer, CountryMap, CountryMapLayer, StateMap, StateMapLayer, CountyMap, CountyMapLayer

app_name = 'corona'

urlpatterns = [
    path('', WorldMap.as_view(), name='world'),
    path('data.geojson/', WorldMapLayer.as_view(), name='world_data'),
    path('<str:country>/', CountryMap.as_view(), name='country'),
    path('<str:country>/data.geojson/', CountryMapLayer.as_view(), name='country_data'),
    path('<str:country>/<str:state>/', StateMap.as_view(), name='state'),
    path('<str:country>/<str:state>/data.geojson/', StateMapLayer.as_view(), name='state_data'),
    path('<str:country>/<str:state>/<str:county>/', CountyMap.as_view(), name='county'),
    path('<str:country>/<str:state>/<str:county>/data.geojson/', CountyMapLayer.as_view(), name='county_data'),
    # path('data.geojson', GeoJSONLayerView.as_view(model=Covid19Info, properties=('combinedKey', 'confirmed', 'deaths', 'recovered', 'active')), name='data')
]
