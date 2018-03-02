from . import *

DEBUG = False
ALLOWED_HOSTS = ['memories.ninja', '54.252.159.196']

# Legacy bucket names
# 'family-photos-prod-orig'
# 'family-photos-prod-thumb'
AWS_STORAGE_BUCKET_NAME = 'family-photos-prod'

DJANGO_SETTINGS_MODULE = 'photos.settings.prod'
CELERY_TASK_ALWAYS_EAGER = False
