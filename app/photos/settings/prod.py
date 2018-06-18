from . import *

DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = [
    'memories.ninja',
    '167.99.78.141',
    '127.0.0.1',
    'localhost',
]

AWS_STORAGE_BUCKET_NAME = 'memories-ninja-prod'

# Logging
LOGGING['root']['handlers'] = ['console', 'sentry']
LOGGING['handlers']['sentry'] = {
    'level': 'ERROR',
    'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
}

RAVEN_CONFIG = {
    'dsn': os.environ.get('PHOTOS_RAVEN_DSN')
}

INSTALLED_APPS.remove('debug_toolbar')
MIDDLEWARE.remove('debug_toolbar.middleware.DebugToolbarMiddleware')
