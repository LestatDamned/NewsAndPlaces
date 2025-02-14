from celery import shared_task

from .models import Place
from .weather_script import fetch_weather


@shared_task()
def get_weather_report():
    """Таска для получения данных о погоде в примечательных местах"""
    places = Place.objects.all()
    try:
        for place in places:
            fetch_weather(place)
    except (ValueError, ConnectionError) as e:
        print(f"Ошибка при получении данных о погоде для места {place.name}: {e}")
        return f"Ошибка: {e}"
