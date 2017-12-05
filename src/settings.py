import os

# TODO - REMOVE WEBSITE_BUCKET
WEBSITE_BUCKET_NAME = os.environ['WEBSITE_BUCKET_NAME']
PHOTO_BUCKET_NAME = os.environ['PHOTO_BUCKET_NAME']
ALLOWED_EXTENSIONS = ('jpeg', 'jpg')
ALLOWED_CONTENT_TYPES = ('image/jpeg',)
THUMBNAIL_HEIGHT = 140  # px

creds, cloud_name = os.environ['CLOUDINARY_URL'].lstrip('cloudinary://').split('@')
CLOUDINARY_URL = 'https://api.cloudinary.com/v1_1/{}/'.format(cloud_name)

from base64 import b64encode
CLOUDINARY_AUTH = 'Basic {}'.format(b64encode(creds))