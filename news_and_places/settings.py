"""
Django settings for news_and_places project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from datetime import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&fv5t4o-&h8rrlj-2lthdpj^7g99g-zwvf!1^uxu+@!ai*6i91'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    'rest_framework',
    'django_summernote',
    'django_celery_beat',
    'django_celery_results',
    'constance',

    'news',
    'places',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'news_and_places.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

WSGI_APPLICATION = 'news_and_places.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": str(os.getenv("POSTGRES_NAME")),
        "USER": str(os.getenv("POSTGRES_USER")),
        "PASSWORD": str(os.getenv("POSTGRES_PASSWORD")),
        "HOST": str(os.getenv("POSTGRES_HOST")),
        "PORT": str(os.getenv("POSTGRES_PORT")),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Krasnoyarsk'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_ADDITIONAL_FIELDS = {
    'choice_period': ['django.forms.fields.ChoiceField', {
        'widget': 'django.forms.Select',
        'choices': ((None, "-----"),
                    ("DAYS", "ДНИ"),
                    ("HOURS", "ЧАСЫ"),
                    ("MINUTES", "МИНУТЫ"),
                    ("SECONDS", "СЕКУНДЫ"),
                    ("MICROSECONDS", "МИКРОСЕКУНДЫ"))
    }],
}

CONSTANCE_CONFIG = {
    'NEWS_RECIPIENTS': ('lestat.one@yandex.ru', 'Список получателей новостей (записывать через запятую)', str),
    'NEWS_SUBJECT': ('Сборник новостей за сегодняшнего дня', 'Тема письма', str),
    'NEWS_TEXT': ('Здравствуйте, подборка новостей за сегодняшний день!', 'Текст письма', str),
    'NEWS_TIME_OF_MESSAGE': (time(12, 00), 'Время отправки сообщения (ЧЧ:ММ)', time),
    'WEATHER_REPORT_INTERVAL': (1, 'Какой интервал ожидания перед повторным запуском задачи', int),
    'WEATHER_REPORT_PERIOD': ("HOURS", 'Тип периода между запусками задач (пример: дни)', 'choice_period')
}

CELERY_BROKER_URL = str(os.getenv("REDIS_HOST"))
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_TIMEZONE = 'Asia/Krasnoyarsk'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CACHES = {
    'default': {
        'BACKEND': "django.core.cache.backends.redis.RedisCache",
        'LOCATION': str(os.getenv("REDIS_CACHES")),
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = str(os.getenv("EMAIL_HOST"))
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = str(os.getenv("EMAIL_HOST_USER"))
EMAIL_HOST_PASSWORD = str(os.getenv("EMAIL_HOST_PASSWORD"))
DEFAULT_FROM_EMAIL = str(os.getenv("DEFAULT_FROM_EMAIL"))
