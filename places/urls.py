from django.urls import path

from .views import ImportPlacesAPIView, WeatherExportAPIView

urlpatterns = [
    path('api/import_places/', ImportPlacesAPIView.as_view(), name='import_places'),
    path('api/export_weather/', WeatherExportAPIView.as_view(), name='export_weather'),
]
