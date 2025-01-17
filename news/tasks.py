from datetime import datetime

from celery import shared_task
from constance import config
from django.conf import settings
from django.core.mail import send_mail

from .models import News


@shared_task
def send_news_email():
    """Таска для отправки рассылки о новостях"""
    today_news = News.objects.filter(publish_date__date=datetime.today().date())
    subject = config.NEWS_SUBJECT
    recipients = config.NEWS_RECIPIENTS.split(",")
    message = config.NEWS_TEXT

    for news in today_news:
        message += f"<hr>Новость: {news.title}<br>Текст: {news.text}Автор: {news.author}"
    send_mail(subject=subject,
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=recipients,
              message=message,
              html_message=message)
