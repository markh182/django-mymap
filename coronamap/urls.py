from django.urls import path
from . import views
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView
from .models import Covid19Info
from .views import CovidMap, MapLayer, CovidMapByCountry, MapLayerByCountry, CovidMapByProvince, MapLayerByProvince

app_name = 'coronamap'

urlpatterns = [
    path('coronamap/', CovidMap.as_view(), name='home'),
    path('data.geojson/', MapLayer.as_view(), name='data'),
    path('coronamap/<str:country>/', CovidMapByCountry.as_view(), name='country'),
    path('<str:country>/data.geojson/', MapLayerByCountry.as_view(), name='databycountry'),
    path('coronamap/<str:country>/<str:province>/', CovidMapByProvince.as_view(), name='province'),
    path('<str:country>/<str:province>/data.geojson/', MapLayerByProvince.as_view(), name='databyprovince'),
    # path('data.geojson', GeoJSONLayerView.as_view(model=Covid19Info, properties=('combinedKey', 'confirmed', 'deaths', 'recovered', 'active')), name='data')
]
