from constance.signals import config_updated
from django.dispatch import receiver
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from django.utils.timezone import now

@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):
    """Сигнал для изменения времени отправки письма при изменении в админке"""
    if key == "NEWS_TIME_OF_MESSAGE":
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=new_value.minute,
            hour=new_value.hour,
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
        )

        task, created = PeriodicTask.objects.get_or_create(
            name="SEND TODAY NEWS EMAIL",
            defaults={
                "task": "news.tasks.send_news_email",
                "crontab": schedule,
                "enabled": True,
                "start_time": now()

            },
        )
        if not created:
            task.crontab = schedule
            task.enabled = True
            task.save()
