from . import *

ALLOWED_HOSTS = ['192.168.2.2']

# Legacy bucket names
# 'family-photos-dev-orig'
# 'family-photos-dev-thumb'
AWS_STORAGE_BUCKET_NAME = 'family-photos-dev'

# Celery
CELERY_TASK_ALWAYS_EAGER = False
