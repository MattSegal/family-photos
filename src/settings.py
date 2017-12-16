import os

# S3 buckets
ORIG_BUCKET_NAME = os.environ['ORIG_BUCKET_NAME']
THUMB_BUCKET_NAME = os.environ['THUMB_BUCKET_NAME']

# DynamoDB tables
IMAGE_TABLE_NAME = 'images'
ALBUM_TABLE_NAME = 'albums'

# Image properties
ALLOWED_EXTENSIONS = ('jpeg', 'jpg')
ALLOWED_CONTENT_TYPES = ('image/jpeg',)
THUMBNAIL_HEIGHT = 140  # px
THUMBNAIL_WIDTH = 225  # px
DISPLAY_HEIGHT = 700 # px
