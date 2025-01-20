import os
import random

import requests
from dotenv import load_dotenv
from requests import HTTPError

from .models import Place, WeatherReport

load_dotenv()

WIND_DIRECTIONS = [
    "Штиль",
    "Северный",
    "Северо-восточный",
    "Восточный",
    "Юго-восточный",
    "Южный",
    "Юго-западный",
    "Западный",
    "Северо-западный",
]


def fetch_weather(place: Place):
    """Получение данных о погоде с API и сохранение в базе данных"""
    key = os.getenv("WEATHER_API_KEY")
    if not key:
        raise ValueError("Не указан API-ключ. Убедитесь, что переменная WEATHER_API_KEY задана в .env файле.")

    lat = place.location.y
    lon = place.location.x
    base_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={key}"

    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except HTTPError as e:
        raise ConnectionError(f"Ошибка при запросе к API: {e}")

    data = response.json()
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind_speed = data["wind"]["speed"]
    wind_direction = random.choice(WIND_DIRECTIONS)

    weather_report = WeatherReport.objects.create(
        place=place,
        temperature=temp,
        humidity=humidity,
        pressure=pressure,
        wind_direction=wind_direction,
        wind_speed=wind_speed
    )

    return weather_report
