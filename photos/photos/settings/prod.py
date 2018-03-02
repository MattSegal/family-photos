from . import *

DEBUG = False
ALLOWED_HOSTS = ['memories.ninja', '54.252.159.196']

AWS_STORAGE_BUCKET_NAME = 'memories-ninja-prod'

DJANGO_SETTINGS_MODULE = 'photos.settings.prod'
CELERY_TASK_ALWAYS_EAGER = False
