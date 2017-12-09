import logging
import sys
from io import BytesIO

import boto3
from PIL import Image, ExifTags

import settings
from utils import download_file_s3, upload_file_s3

ORIENTATION = next(k for k in ExifTags.TAGS.keys() if ExifTags.TAGS[k] == 'Orientation')
log = logging.getLogger(__name__)
orig_bucket = boto3.resource('s3').Bucket(settings.ORIG_BUCKET_NAME)
thumb_bucket = boto3.resource('s3').Bucket(settings.THUMB_BUCKET_NAME)


def resize_image(filename):
    """
    Download original image from S3, thumbnail it, and upload thumbnail
    """
    log.debug('Resizing image %s', filename)
    # Read image into memory from S3
    key = 'original/{}'.format(filename)
    file_obj = download_file_s3(key, orig_bucket)

    # Thumbnail the image and upload to S3
    img = Image.open(file_obj)
    img = ensure_image_upright(img)
    img.thumbnail((sys.maxint, settings.THUMBNAIL_HEIGHT), Image.ANTIALIAS)
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    upload_file_s3(
       filename=filename,
       path='thumbnail',
       file_obj=img_bytes,
       bucket=thumb_bucket
    )

    # Make a display size image and upload to S3
    img = Image.open(file_obj)
    img = ensure_image_upright(img)
    img.thumbnail((sys.maxint, settings.DISPLAY_HEIGHT), Image.ANTIALIAS)
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    upload_file_s3(
       filename=filename,
       path='display',
       file_obj=img_bytes,
       bucket=thumb_bucket
    )



def ensure_image_upright(img):
    """
    Make sure the image is the right way up
    """
    exif = img._getexif()
    if not exif:
        return img

    exif = dict(exif.items())

    if exif[ORIENTATION] == 3:
        return img.rotate(180, expand=True)
    elif exif[ORIENTATION] == 6:
        return img.rotate(270, expand=True)
    elif exif[ORIENTATION] == 8:
        return img.rotate(90, expand=True)
    else:
        return img
