from constance import config
from constance.signals import config_updated
from django.dispatch import receiver
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from django.utils.timezone import now


@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):
    """Сигнал для изменения интервала проверки погоды при изменении в админке"""

    interval_mapping = {
        "SECONDS": IntervalSchedule.SECONDS,
        "MINUTES": IntervalSchedule.MINUTES,
        "HOURS": IntervalSchedule.HOURS,
        "DAYS": IntervalSchedule.DAYS,
        "MICROSECONDS": IntervalSchedule.MICROSECONDS,
    }

    new_interval = config.WEATHER_REPORT_INTERVAL
    new_period = config.WEATHER_REPORT_PERIOD


    if key == "WEATHER_REPORT_INTERVAL":
        new_interval = new_value
    if key == "WEATHER_REPORT_PERIOD":
        new_period = new_value
        new_period = interval_mapping.get(new_period, IntervalSchedule.HOURS)

        interval, _ = IntervalSchedule.objects.get_or_create(
                every=new_interval,
                period=new_period,
        )

        task, created = PeriodicTask.objects.get_or_create(
            name="WEATHER CHECK",
            defaults={
                "task": "places.tasks.get_weather_report",
                "interval": interval,
                "enabled": True,
                "start_time": now()
            },
        )
        if not created:
            task.interval = interval
            task.enabled = True
            task.save()
