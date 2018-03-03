from . import *

DEBUG = False
ALLOWED_HOSTS = ['memories.ninja', '54.252.159.196']

AWS_STORAGE_BUCKET_NAME = 'memories-ninja-prod'

DJANGO_SETTINGS_MODULE = 'photos.settings.prod'
CELERY_TASK_ALWAYS_EAGER = False


# Logging
LOGGING['root']['handlers'] = ['console', 'sentry']
LOGGING['handlers']['sentry'] = {
    'level': 'ERROR',
    'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
}

RAVEN_CONFIG = {
    'dsn': os.environ.get('RAVEN_DSN')
}
