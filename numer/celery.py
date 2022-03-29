from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
# если мы запускаем celery из коммандной строки без указания файла настроек
# в случае деполя в продакшне, celery запускается как демон с указанием файла настроек
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'numer.settings')

app = Celery('numer')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
