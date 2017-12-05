import os

# TODO - REMOVE WEBSITE_BUCKET
WEBSITE_BUCKET_NAME = os.environ['WEBSITE_BUCKET_NAME']
PHOTO_BUCKET_NAME = os.environ['PHOTO_BUCKET_NAME']
ALLOWED_EXTENSIONS = ('jpeg', 'jpg')
ALLOWED_CONTENT_TYPES = ('image/jpeg',)
THUMBNAIL_HEIGHT = 140  # px
