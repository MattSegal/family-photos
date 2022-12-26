import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from . import *

DEBUG = False
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = [
    "memories.ninja",
    "167.179.136.207",
    "127.0.0.1",
    "localhost",
]

AWS_STORAGE_BUCKET_NAME = "memories-ninja-prod"

sentry_sdk.init(
    dsn=os.environ.get("RAVEN_DSN"), integrations=[DjangoIntegration()], environment="prod"
)

INSTALLED_APPS.remove("debug_toolbar")
MIDDLEWARE.remove("debug_toolbar.middleware.DebugToolbarMiddleware")
