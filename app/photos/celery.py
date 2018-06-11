import os
from celery import Celery
from django.conf import settings

from photos.images import thumbnail

celery_host = os.environ.get('CELERY_HOST')
app = Celery('photos', broker='redis://{}:6379'.format(celery_host))
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
