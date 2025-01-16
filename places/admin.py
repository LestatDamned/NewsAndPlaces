from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import Place, WeatherReport


@admin.register(Place)
class PlaceAdmin(GISModelAdmin):
    """Настройка отображения модели Place в админке"""

    list_display = ('id', 'name', 'rating', 'location')
    search_fields = ('name',)
    list_filter = ('rating',)


@admin.register(WeatherReport)
class WeatherReportAdmin(admin.ModelAdmin):
    """Настройка отображения модели WeatherReport в админке"""
    list_display = (
        'id',
        'place',
        'temperature',
        'humidity',
        'pressure',
        'wind_direction',
        'wind_speed',
        'created_at',
    )
    readonly_fields = (
        'place',
        'temperature',
        'humidity',
        'pressure',
        'wind_direction',
        'wind_speed',
        'created_at',
    )
    search_fields = ('place__name',)
    list_filter = ('place', 'created_at',)
