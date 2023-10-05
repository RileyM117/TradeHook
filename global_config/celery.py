import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','global_config.settings.dev')

celery = Celery('global_config')
celery.config_from_object('django.conf:settings',namespace='CELERY')
celery.autodiscover_tasks()