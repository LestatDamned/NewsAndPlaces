from django.contrib.gis.db import models as geomodels
from django.db import models


class Place(models.Model):
    """Модель для примечательных мест"""
    name = models.CharField(max_length=255, verbose_name="Название места")
    location = geomodels.PointField(verbose_name="Координаты места")
    rating = models.IntegerField(choices=[(i, i) for i in range(26)], default=0, verbose_name="Рейтинг места")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Примечательное место"
        verbose_name_plural = "Примечательные места"



class WeatherReport(models.Model):
    """Модель погоды"""
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="weather_reports",
                              verbose_name="Примечательное место")
    temperature = models.FloatField(verbose_name="Температура по шкале Цельсия")
    humidity = models.IntegerField(verbose_name="Влажность воздуха, в %")
    pressure = models.FloatField(verbose_name="Атмосферное давление, в мм ртутного столба")
    wind_direction = models.CharField(max_length=100, verbose_name="Направление ветра")
    wind_speed = models.FloatField(verbose_name="Скорость ветра, в м/с")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата снятия показаний")

    def __str__(self):
        return f"Погода для {self.place.name} от {self.created_at}"

    class Meta:
        verbose_name = "Сводка погоды"
        verbose_name_plural = "Сводки погоды"
