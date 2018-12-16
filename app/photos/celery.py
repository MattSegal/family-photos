import os
from celery import Celery
from django.conf import settings

from photos.images import thumbnail

celery_host = os.environ.get('CELERY_HOST')
broker_url = f'redis://{celery_host}:6379'
app = Celery('photos', broker=broker_url)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.result_backend = broker_url
